#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_policy_access_rule import PolicyAccessRuleService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_policy_access_rule_info
short_description: Retrieves policy access rule information.
description:
  - This module will allow the retrieval of information about a policy access rule.
author: William Guilherme (@willguibr)
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
- name: Get Details of All Policy Access Rules
    willguibr.zpacloud.zpa_policy_access_rule_info:
    
- name: Get Details of a Policy Access Rule by Name
    willguibr.zpacloud.zpa_policy_access_rule_info:
    name: "Policy Access Rule - Example"
    
- name: Get Details of a Policy Access Rule by ID
    willguibr.zpacloud.zpa_policy_access_rule_info:
    id: "216196257331291979"
"""

RETURN = """
# Returns information on a specified Policy Access Rule.
"""


def core(module):
    policy_rule_name = module.params.get("name", None)
    policy_rule_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = PolicyAccessRuleService(module, customer_id)
    global_policy_set = service.getByPolicyType("ACCESS_POLICY")
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
            policy_rule_name, "ACCESS_POLICY")
        if policy_rule is None:
            module.fail_json(
                msg="Failed to retrieve policy rule Name: '%s'" % (policy_rule_name))
        policy_rules = [policy_rule]
    else:
        policy_rules = service.getAllByPolicyType("ACCESS_POLICY")
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
