#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_policy_forwarding_rule import PolicyForwardingRuleService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_policy_forwarding_rule
short_description: Create a Policy Forwarding Rule.
description:
  - This module will create, update or delete a specific Policy Forwarding Rule
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
    description:
      - This is for providing the rule action.
    choices:
      - INTERCEPT
      - INTERCEPT_ACCESIBLE
      - BYPASS
  action_id:
    type: str
    required: False
    description:
      - This field defines the description of the server.
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
    description:
      - This is for providing a customer message for the user.
  operator:
    description:
      - This denotes the operation type.
    type: str
    required: False
    choices:
      - AND
      - OR
  custom_msg:
    type: str
    required: False
    description:  "This is for providing a customer message for the user."
  name:
    type: str
    required: True
    description:  "This is the name of the policy."
  description:
    type: str
    required: false
    description:
      - This is the description of the access policy.
  conditions:
    type: list
    elements: dict
    required: false
    description:
      - This is for proviidng the set of conditions for the policy.
    suboptions:
      negated:
        type: bool
        required: false
        description:
          - ""
      operator:
        description:
          - This denotes the operation type.
        type: str
        required: false
        choices:
          - AND
          - OR
        suboptions:
          operands:
            type: list
            elements: str
            required: false
            description:
              - This signifies the various policy criterias.
            suboptions:
              idp_id:
                type: str
                required: false
                description:
                  - ""
              lhs:
                type: str
                required: false
                description:
                  - This signifies the key for the object type.
              name:
                type: str
                required: false
                description:
                  - This signifies the key for the object type.
              rhs:
                type: str
                required: false
                description:
                  - This denotes the value for the given object type. Its value depends upon the key.
              object_type:
                type: str
                required: false
                description:
                  - This is for specifying the policy criteria.
                choices:
                  - APP
                  - APP_GROUP
                  - BYPASS
                  - SAML
                  - IDP
                  - CLIENT_TYPE
                  - TRUSTED_NETWORK
                  - MACHINE_GRP
                  - POSTURE
                  - SCIM
                  - SCIM_GROUP
                  - EDGE_CONNECTOR_GROUP
"""

EXAMPLES = """
- name: Policy Forwarding Rule - Example
  willguibr.zpacloud.zpa_policy_forwarding_rule:
    name: "Policy Forwarding Rule - Example"
    description: "Policy Forwarding Rule - Example"
    action: "BYPASS"
    rule_order: 1
    operator: "AND"
    conditions:
      - negated: false
        operator: "OR"
        operands:
          - name: "app_segment"
            object_type: "APP"
            lhs: "id"
            rhs: "216196257331292105"
          - name: "segment_group"
            object_type: "APP_GROUP"
            lhs: "id"
            rhs: "216196257331292103"
      - negated: false
        operator: "OR"
        operands:
          - name: "zpn_client_type_exporter"
            object_type: "CLIENT_TYPE"
            lhs: "id"
            rhs: "zpn_client_type_exporter"
          - name: "zpn_client_type_browser_isolation"
            object_type: "CLIENT_TYPE"
            lhs: "id"
            rhs: "zpn_client_type_browser_isolation"
          - name: "zpn_client_type_zapp"
            object_type: "CLIENT_TYPE"
            lhs: "id"
            rhs: "zpn_client_type_zapp"
      - negated: false
        operator: "OR"
        operands:
          - name: "CrowdStrike_ZPA_ZTA_80"
            object_type: "POSTURE"
            lhs: "{{ postures.data[0].posture_udid }}"
            rhs: "false"
"""

RETURN = r"""
data:
    description: Policy Forwarding Rule
    returned: success
    type: dict
    sample:
        {
        }
"""


def core(module):
    state = module.params.get("state", None)
    customer_id = module.params.get("customer_id", None)
    service = PolicyForwardingRuleService(module, customer_id)
    global_policy_set = service.getByPolicyType("BYPASS_POLICY")
    if global_policy_set is None or global_policy_set.get("id") is None:
        module.fail_json(msg="Unable to get global policy set")
    policy_set_id = global_policy_set.get("id")
    policy = dict()
    params = [
        "id",
        "name",
        "description",
        "action",
        "action_id",
        "default_rule",
        "default_rule_name",
        "bypass_default_rule",
        "policy_type",
        "policy_set_id",
        "custom_msg",
        "priority",
        "operator",
        "rule_order",
        "conditions",
    ]
    for param_name in params:
        policy[param_name] = module.params.get(param_name, None)
    existing_policy = service.getByIDOrName(
        policy.get("id"), policy.get("name"), policy_set_id, "BYPASS_POLICY")
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
    argument_spec.update(
        id=dict(type='str'),
        name=dict(type='str', required=True),
        description=dict(type='str', required=False),
        action=dict(type='str', required=False, choices=["INTERCEPT", "INTERCEPT_ACCESSIBLE", "BYPASS"], default="INTERCEPT"),
        action_id=dict(type='str', required=False),
        default_rule=dict(type='bool', required=False),
        default_rule_name=dict(type='str', required=False),
        custom_msg=dict(type='str', required=False),
        bypass_default_rule=dict(type='bool', required=False),
        operator=dict(type='str', required=False),
        policy_type=dict(type='str', required=False),
        priority=dict(type='str', required=False),
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
