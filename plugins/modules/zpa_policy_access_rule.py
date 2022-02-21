#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

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
  client_id:
    description: ""
    required: false
    type: str
  client_secret:
    description: ""
    required: false
    type: str
  customer_id:
    description: ""
    required: false
    type: str
  action:
    description:
      - This is for providing the rule action.
    type: str
    required: false
    choices:
      - ALLOW
      - DENY
  action_id:
    type: str
    required: false
    description:
      - This field defines the description of the server.
  priority:
    description: ""
    type: str
    required: false
  id:
    type: str
    description: ""
  default_rule_name:
    type: str
    description: ""
  description:
    type: str
    description: ""
  policy_type:
    description: ""
    type: str
    required: false
  rule_order:
    description: ""
    type: str
    required: false
  default_rule:
    description:
      - This is for providing a customer message for the user.
    type: bool
    required: false
  operator:
    description:
      - This denotes the operation type.
    type: str
    required: false
    choices:
      - AND
      - OR
  app_connector_groups:
    description:
      - List of the app connector group IDs.
    type: list
    elements: dict
    required: false
    suboptions:
      name:
        required: false
        type: str
        description: ""
      id:
        required: true
        type: str
        description: ""
  app_server_groups:
    type: list
    elements: dict
    required: false
    description:
      - List of the server group IDs.
    suboptions:
      name:
        required: false
        type: str
        description: ""
      id:
        required: true
        type: str
        description: ""
  custom_msg:
    description:
      - This is for providing a customer message for the user.
    type: str
    required: false
  lss_default_rule:
    description: ""
    type: bool
    required: False
  name:
    description:
      - This is the name of the policy.
    type: str
    required: True
  conditions:
    type: list
    elements: dict
    required: False
    description: ""
    suboptions:
      id:
        description: ""
        type: str
      negated:
        description: ""
        type: bool
        required: False
      operator:
        description: ""
        type: str
        required: True
        choices: ["AND", "OR"]
      operands:
        required: False
        description: ""
        type: list
        elements: dict
        suboptions:
          id:
            description: ""
            type: str
          idp_id:
            description: ""
            type: str
            required: False
          name:
            description: ""
            type: str
            required: False
          lhs:
            description: ""
            type: str
            required: True
          rhs:
            description: ""
            type: str
            required: False
          rhs_list:
            description: ""
            type: list
            elements: str
            required: False
          object_type:
            description: ""
            type: str
            required: True
            choices:
              - APP
              - APP_GROUP
              - SAML
              - IDP
              - CLIENT_TYPE
              - TRUSTED_NETWORK
              - MACHINE_GRP
              - POSTURE
              - SCIM
              - SCIM_GROUP
              - EDGE_CONNECTOR_GROUP
  state:
    description: "Whether the app should be present or absent."
    type: str
    choices:
        - present
        - absent
    default: present
"""

EXAMPLES = """
- name: Access Policy - Intranet Web Apps
  willguibr.zpacloud.zpa_policy_access_rule:
    name: "Intranet Web Apps"
    description: "Intranet Web Apps"
    action: "ALLOW"
    rule_order: 1
    operator: "AND"
    conditions:
      - negated: false
        operator: "OR"
        operands:
          - name: "app_seg_intranet"
            object_type: "APP"
            lhs: "id"
            rhs: "{{ app_seg_intranet.data.id }}"
      - negated: false
        operator: "OR"
        operands:
          - name: "sg_seg_intranet"
            object_type: "APP_GROUP"
            lhs: "id"
            rhs: "{{ seg_intranet.data.id }}"
      - negated: false
        operator: "OR"
        operands:
          - name: "engineering_group"
            object_type: "SCIM_GROUP"
            lhs: "{{ user_okta.data[0].id }}"
            rhs: "{{ engineering_group.data[0].id }}"
"""

RETURN = """
# The newly created policy access rule resource record.
"""

from traceback import format_exc

from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper,
)
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_policy_access_rule import (
    PolicyAccessRuleService,
)


def core(module):
    state = module.params.get("state", None)
    customer_id = module.params.get("customer_id", None)
    service = PolicyAccessRuleService(module, customer_id, ZPAClientHelper(module))
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
        "lss_default_rule",
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
        policy.get("id"), policy.get("name"), policy_set_id, "ACCESS_POLICY"
    )
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
            module.exit_json(changed=True, data=existing_policy)
    module.exit_json(changed=False, data={})


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    id_name_spec = dict(
        type="list",
        elements="dict",
        options=dict(
            id=dict(type="str", required=True), name=dict(type="str", required=False)
        ),
        required=False,
    )
    argument_spec.update(
        default_rule=dict(type="bool", required=False),
        default_rule_name=dict(type="str", required=False),
        description=dict(type="str", required=False),
        policy_type=dict(type="str", required=False),
        custom_msg=dict(type="str", required=False),
        # policy_set_id=dict(type='str', required=True),
        id=dict(type="str"),
        lss_default_rule=dict(type="bool", required=False),
        action_id=dict(type="str", required=False),
        name=dict(type="str", required=True),
        app_connector_groups=id_name_spec,
        action=dict(type="str", required=False, choices=["ALLOW", "DENY"]),
        priority=dict(type="str", required=False),
        operator=dict(type="str", required=False, choices=["AND", "OR"]),
        rule_order=dict(type="str", required=False),
        conditions=dict(
            type="list",
            elements="dict",
            options=dict(
                id=dict(type="str"),
                negated=dict(type="bool", required=False),
                operator=dict(type="str", required=True, choices=["AND", "OR"]),
                operands=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        id=dict(type="str"),
                        idp_id=dict(type="str", required=False),
                        name=dict(type="str", required=False),
                        lhs=dict(type="str", required=True),
                        rhs=dict(type="str", required=False),
                        rhs_list=dict(type="list", elements="str", required=False),
                        object_type=dict(
                            type="str",
                            required=True,
                            choices=[
                                "APP",
                                "APP_GROUP",
                                "SAML",
                                "IDP",
                                "CLIENT_TYPE",
                                "TRUSTED_NETWORK",
                                "MACHINE_GRP",
                                "POSTURE",
                                "SCIM",
                                "SCIM_GROUP",
                                "EDGE_CONNECTOR_GROUP",
                            ],
                        ),
                    ),
                    required=False,
                ),
            ),
            required=False,
        ),
        app_server_groups=id_name_spec,
        state=dict(type="str", choices=["present", "absent"], default="present"),
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
