#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_policy_forwarding_rule import PolicyForwardingRuleService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_policy_forwarding_rule_info
short_description: Retrieves policy forwarding rule information.
description:
  - This module will allow the retrieval of information about a policy forwarding rule.
author: William Guilherme (@willguibr)
version_added: "1.0.0"
requirements:
  - supported starting from zpa_api >= 1.0
options:
  name:
    description:
      - Name of the policy forwarding rule.
    required: true
    type: str
  id:
    description:
      - ID of the policy forwarding rule.
    required: false
    type: str
"""

EXAMPLES = """
- name: Get Information About All Policy Forwarding Rules
    willguibr.zpacloud.zpa_policy_forwarding_rule_info:
  
- name: Get information About Forwarding Rules by Name
    willguibr.zpacloud.zpa_policy_forwarding_rule_info:
      name: "All Other Services"
    
- name: Get information About Forwarding Rules by ID
    willguibr.zpacloud.zpa_policy_forwarding_rule_info:
      id: "216196257331292020"
"""

RETURN = """
# Returns information on a specified policy forwarding rule.
"""


def core(module):
    policy_rule_name = module.params.get("name", None)
    policy_rule_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = PolicyForwardingRuleService(module, customer_id)
    global_policy_set = service.getByPolicyType("BYPASS_POLICY")
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
            policy_rule_name, "BYPASS_POLICY")
        if policy_rule is None:
            module.fail_json(
                msg="Failed to retrieve policy rule Name: '%s'" % (policy_rule_name))
        policy_rules = [policy_rule]
    else:
        policy_rules = service.getAllByPolicyType("BYPASS_POLICY")
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
