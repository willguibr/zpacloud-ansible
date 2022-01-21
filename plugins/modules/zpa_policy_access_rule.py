#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_policy_access_rule import PolicyAccessRuleService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_policy_access_rule
short_description: Create a Policy Access Rule
description:
  - This module create/update/delete a Policy Access Rule in the ZPA Cloud.
author:
  - William Guilherme (@willguibr)
version_added: "1.0.0"
options:
  bypass_default_rule:
    type: bool
    required: False
    description: ""
  policy_set_id:
    type: str
    required: True
    description: ""
  action:
    type: str
    required: False
    description:  "  This is for providing the rule action."
  action_id:
    type: str
    required: False
    description:  "This field defines the description of the server."
  priority:
    type: str
    required: False
    description: ""
  id:
    type: str
    description: ""
  policy_type:
    type: str
    required: False
    description: ""
  rule_order:
    type: str
    required: False
    description: ""
  default_rule:
    type: bool
    required: False
    description:  "This is for providing a customer message for the user."
  operator:
    type: str
    required: False
    description: ""
  app_connector_groups:
    type: list
    elements: dict
    required: False
    description:  "List of app-connector IDs."
  reauth_default_rule:
    type: bool
    required: False
    description: ""
  description:
    type: str
    required: False
    description:  "This is the description of the access policy."
  conditions:
    type: list
    elements: dict
    required: False
    description:  "This is for proviidng the set of conditions for the policy."
  reauth_idle_timeout:
    type: str
    required: False
    description: ""
  app_server_groups:
    type: list
    elements: dict
    required: False
    description:  "List of the server group IDs."
  reauth_timeout:
    type: str
    required: False
    description: ""
  custom_msg:
    type: str
    required: False
    description:  "This is for providing a customer message for the user."
  lss_default_rule:
    type: bool
    required: False
    description: ""
  name:
    type: str
    required: True
    description:  "This is the name of the policy."
"""

EXAMPLES = """
    - name: Create/Update/Delete a Policy Access Rule
      willguibr.zpacloud.zpa_policy_access_rule:
        name: "Policy Access Rule - Example"
        description: "Policy Access Rule - Example"
        action: "ALLOW"
        rule_order: 2
        operator: "AND"
        conditions:
          - negated: false
            operator: "OR"
            operands:
              - name: "app_segment"
                object_type: "APP"
                lhs: "id"
                rhs: "216196257331291979"
        state: present
      register: created_rule
    - name: created policy access rule
      debug:
        msg: "{{ created_rule }}"
"""

RETURN = """
data:
    description: Policy Rule
    returned: success
    type: dict
    sample:
        {
        }
"""


def core(module):
    state = module.params.get("state", None)
    customer_id = module.params.get("customer_id", None)
    service = PolicyAccessRuleService(module, customer_id)
    global_policy_set = service.getByPolicyType("ACCESS_POLICY")
    if global_policy_set is None or global_policy_set.get("id") is None:
        module.fail_json(msg="Unable to get global policy set")
    policy_set_id = global_policy_set.get("id")
    policy = dict()
    params = [
        "default_rule",
        "description",
        "policy_type",
        "custom_msg",
        "policy_set_id",
        "id",
        "reauth_default_rule",
        "lss_default_rule",
        "bypass_default_rule",
        "reauth_idle_timeout",
        "reauth_timeout",
        "action_id",
        "name",
        "app_connector_groups",
        "action",
        "priority",
        "operator",
        "rule_order",
        "conditions",
        "app_server_groups",
    ]
    for param_name in params:
        policy[param_name] = module.params.get(param_name, None)
    existing_policy = service.getByIDOrName(
        policy.get("id"), policy.get("name"), policy_set_id, "ACCESS_POLICY")
    if existing_policy is not None:
        id = existing_policy.get("id")
        existing_policy.update(policy)
        existing_policy["id"] = id
    if state == "present":
        if existing_policy is not None:
            """Update"""
            existing_policy = service.update(existing_policy, policy_set_id)
            module.exit_json(changed=True, data=existing_policy)
        else:
            """Create"""
            policy = service.create(policy, policy_set_id)
            module.exit_json(changed=False, data=policy)
    elif state == "absent":
        if existing_policy is not None:
            service.delete(existing_policy.get("id"), policy_set_id)
            module.exit_json(changed=False, data=existing_policy)
    module.exit_json(changed=False, data={})


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    id_name_spec = dict(type='list', elements='dict', options=dict(id=dict(
        type='str', required=True), name=dict(type='str', required=False)), required=False)
    argument_spec.update(
        default_rule=dict(type='bool', required=False),
        description=dict(type='str', required=False),
        policy_type=dict(type='str', required=False),
        custom_msg=dict(type='str', required=False),
        #policy_set_id=dict(type='str', required=True),
        id=dict(type='str'),
        reauth_default_rule=dict(type='bool', required=False),
        lss_default_rule=dict(type='bool', required=False),
        bypass_default_rule=dict(type='bool', required=False),
        reauth_idle_timeout=dict(type='str', required=False),
        reauth_timeout=dict(type='str', required=False),
        action_id=dict(type='str', required=False),
        name=dict(type='str', required=True),
        app_connector_groups=id_name_spec,
        action=dict(type='str', required=False, choices=["ALLOW", "DENY"]),
        priority=dict(type='str', required=False),
        operator=dict(type='str', required=False),
        rule_order=dict(type='str', required=False),
        conditions=dict(type='list', elements='dict', options=dict(id=dict(type='str'),
                                                                   negated=dict(
                                                                       type='bool', required=False),
                                                                   operator=dict(
                                                                       type='str', required=True),
                                                                   operands=dict(type='list', elements='dict', options=dict(id=dict(type='str'),
                                                                                                                            idp_id=dict(
                                                                                                                                type='str', required=False),
                                                                                                                            name=dict(
                                                                                                                                type='str', required=False),
                                                                                                                            lhs=dict(
                                                                                                                                type='str', required=True),
                                                                                                                            rhs=dict(
                                                                                                                                type='str', required=False),
                                                                                                                            rhs_list=dict(
                                                                       type='list', elements='str', required=False),
                                                                       object_type=dict(
                                                                           type='str', required=True),
                                                                   ), required=False),
                                                                   ), required=False),
        app_server_groups=id_name_spec,
        state=dict(type="str", choices=[
                   "present", "absent"], default="present"),
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
