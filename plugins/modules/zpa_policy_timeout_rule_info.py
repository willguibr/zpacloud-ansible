#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_policy_timeout_rule import PolicyTimeOutRuleService
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = r"""
---
author: William Guilherme (@willguibr)
description:
  - Provides details about a specific policy rule created in the Zscaler Private Access Mobile Portal
module: zpa_policy_rule_info
short_description: Provides details about a specific policy rule created in the Zscaler Private Access Mobile Portal
version_added: "1.0.0"
requirements:
  - supported starting from zpa_api >= 1.0
options:
  name:
    description:
      - Name of the policy rule.
    required: false
    type: str
  id:
    description:
      - ID of the policy rule.
    required: false
    type: str
"""

EXAMPLES = """
- name: policy rule
  hosts: localhost
  tasks:
    - name: Gather information about all policy rules
      willguibr.zpacloud_ansible.zpa_policy_access_rule_info:
        #id: "216196257331292020"
        name: "All Other Services"
      register: policy
    - name: policy rule
      debug:
        msg: "{{ policy }}"

"""

RETURN = r"""
data:
    description: policy rule information
    returned: success
    elements: dict
    type: list
    sample:
        [
            {
                "action": "ALLOW",
                "action_id": null,
                "app_connector_groups": [
                    {
                        "city_country": "Langley, CA",
                        "country_code": "CA",
                        "creation_time": "1639693615",
                        "description": "Canada App Connector Group",
                        "dns_query_type": "IPV4",
                        "enabled": true,
                        "id": "216196257331291924",
                        "location": "Langley City, BC, Canada",
                        "lss_app_connector_group": false,
                        "modified_by": "216196257331282070",
                        "name": "Canada App Connector Group",
                        "override_version_profile": true,
                        "version_profile_id": "2"
                    }
                ],
                "app_server_groups": [
                    {
                        "config_space": "DEFAULT",
                        "creation_time": "1639693619",
                        "description": "All Other Services",
                        "dynamic_discovery": true,
                        "enabled": true,
                        "id": "216196257331291967",
                        "modified_by": "216196257331282070",
                        "name": "All Other Services"
                    }
                ],
                "bypass_default_rule": null,
                "conditions": [
                    {
                        "creation_time": "1640027085",
                        "id": "1004465",
                        "modified_by": "216196257331282070",
                        "modified_time": "1640027085",
                        "negated": false,
                        "operands": [
                            {
                                "creation_time": "1640027085",
                                "id": "1004466",
                                "lhs": "id",
                                "modified_by": "216196257331282070",
                                "name": "All Other Services",
                                "object_type": "APP",
                                "rhs": "216196257331291979"
                            },
                            {
                                "creation_time": "1640027085",
                                "id": "1004467",
                                "lhs": "id",
                                "modified_by": "216196257331282070",
                                "name": "All Other Services",
                                "object_type": "APP_GROUP",
                                "rhs": "216196257331291913"
                            }
                        ],
                        "operator": "OR"
                    }
                ],
                "custom_msg": null,
                "default_rule": false,
                "description": "All Other Services",
                "id": "216196257331292020",
                "lss_default_rule": null,
                "name": "All Other Services",
                "operator": "AND",
                "policy_set_id": null,
                "policy_type": "1",
                "priority": "1",
                "reauth_default_rule": null,
                "reauth_idle_timeout": null,
                "reauth_timeout": null,
                "rule_order": "12"
            }
        ]

"""


def core(module):
    policy_rule_name = module.params.get("name", None)
    policy_rule_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = PolicyTimeOutRuleService(module, customer_id)
    global_policy_set = service.getByPolicyType("TIMEOUT_POLICY")
    if global_policy_set is None or global_policy_set.get("id") is None:
        module.fail_json(msg="Unable to get global policy set")
    policy_set_id = global_policy_set.get("id")
    policy_rules = []
    if policy_rule_id is not None:
        policy_rule = service.getByID(policy_rule_id, policy_set_id)
        if policy_rule is None:
            module.fail_json(
                msg="Failed to retrieve policy rule ID: '%s'" % (id))
        policy_rules = [policy_rule]
    elif policy_rule_name is not None:
        policy_rule = service.getByNameAndType(
            policy_rule_name, "TIMEOUT_POLICY")
        if policy_rule is None:
            module.fail_json(
                msg="Failed to retrieve policy rule Name: '%s'" % (policy_rule_name))
        policy_rules = [policy_rule]
    else:
        policy_rules = service.getAllByPolicyType("TIMEOUT_POLICY")
    module.exit_json(changed=False, data=policy_rules)


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    argument_spec.update(
        name=dict(type="str", required=False),
        id=dict(type="str", required=False),
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
