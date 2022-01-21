#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_lss_config_controller import LSSConfigControllerService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper

__metaclass__ = type

DOCUMENTATION = """
---
"""

def core(module):
    state = module.params.get("state", None)
    customer_id = module.params.get("customer_id", None)
    service = LSSConfigControllerService(module, customer_id)
    app = dict()
    params = [
        "id",
        "config",
        "connector_groups",
        "policy_rule_resource"
        "enabled",
        "city_country",
        "country_code",
        "latitude",
        "longitude",
        "location",
        "upgrade_day",
        "upgrade_time_in_secs",
        "override_version_profile",
        "version_profile_id",
        "dns_query_type",
    ]
    for param_name in params:
        app[param_name] = module.params.get(param_name, None)
    existing_app = service.getByIDOrName(app.get("id"), app.get("name"))
    if existing_app is not None:
        id = existing_app.get("id")
        existing_app.update(app)
        existing_app["id"] = id
    if state == "present":
        if existing_app is not None:
            """Update"""
            service.update(existing_app)
            module.exit_json(changed=True, data=existing_app)
        else:
            """Create"""
            app = service.create(app)
            module.exit_json(changed=False, data=app)
    elif state == "absent":
        if existing_app is not None:
            service.delete(existing_app.get("id"))
            module.exit_json(changed=False, data=existing_app)
    module.exit_json(changed=False, data={})


def main():
    """Main"""
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    id_name_spec = dict(type='list', elements='dict', options=dict(id=dict(
        type='str', required=True), name=dict(type='str', required=False)), required=False)
    argument_spec.update(
        config=dict(
            type='dict',
            options=dict(
                audit_message=dict(type="str", required=False),
                creation_time=dict(type="str", required=False),
                description=dict(type="str", required=False),
                enabled=dict(type="bool", default=True, required=False),
                filter=dict(type="str", required=False),
                format=dict(type="str", required=False),
                id=dict(type="str", required=False),
                modified_by=dict(type="str", required=False),
                modified_time=dict(type="str", required=False),
                name=dict(type="str", required=True),
                lss_host=dict(type="str", required=True),
                lss_port=dict(type="str", required=True),
                source_log_type=dict(choices=['zpn_trans_log', 'zpn_auth_log', 'zpn_ast_auth_log', 'zpn_http_trans_log', 'zpn_audit_log', 'zpn_sys_auth_log', 'zpn_http_insp', 'zpn_ast_comprehensive_stats']),
                use_tls=dict(type="bool", required=False),
                ),
            ),
        policy_rule_resource=dict(
            type='dict',
            options=dict(
                action=dict(type='str', required=False, choices=["ALLOW", "DENY"]),
                #policy_set_id=dict(type='str', required=True),
                id=dict(type='str'),
                conditions=dict(type='list', elements='dict', options=dict(id=dict(type='str'),
                                                                   negated=dict(
                                                                       type='bool', required=False),
                                                                   operator=dict(
                                                                       type='str', required=False),
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
                                                                        type='str', required=False, choices=["APP", "APP_GROUP", "CLIENT_TYPE"]),
                                                                   ), required=False),
                                                                   ), required=False),
                ),
            ),
        app_connector_groups=id_name_spec,
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