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
module: zpa_lss_config_controller
short_description: Create a LSS CONFIG.
description:
  - This module create/update/delete a LSS CONFIG in the ZPA Cloud.
author:
  - William Guilherme (@willguibr)
version_added: "1.0.0"
options:
  id:
    type: str
    description: ""
  policy_rule_resource:
    type: list
    elements: dict
    required: False
    description: ""
  connector_groups:
    type: list
    elements: dict
    required: False
    description:  "App Connector Group(s) to be added to the LSS configuration"
  config:
    type: list
    elements: dict
    required: False
    description: ""
"""
EXAMPLES = '''
- name: LSS Controller
  hosts: localhost
  tasks:
    - name: Create a LSS Controller
      willguibr.zpacloud.zpa_lss_config_controller:
        state: present
        config:
          name: Status
          description: status
          enabled: true
          lss_host: 10.1.1.1
          lss_port: 20000
          format: {\"LogTimestamp\": %j{LogTimestamp:time},\"Customer\": %j{Customer},\"SessionID\": %j{SessionID},\"SessionType\": %j{SessionType},\"SessionStatus\": %j{SessionStatus},\"Version\": %j{Version},\"Platform\": %j{Platform},\"ZEN\": %j{ZEN},\"Connector\": %j{Connector},\"ConnectorGroup\": %j{ConnectorGroup},\"PrivateIP\": %j{PrivateIP},\"PublicIP\": %j{PublicIP},\"Latitude\": %f{Latitude},\"Longitude\": %f{Longitude},\"CountryCode\": %j{CountryCode},\"TimestampAuthentication\": %j{TimestampAuthentication:iso8601},\"TimestampUnAuthentication\": %j{TimestampUnAuthentication:iso8601},\"CPUUtilization\": %d{CPUUtilization},\"MemUtilization\": %d{MemUtilization},\"ServiceCount\": %d{ServiceCount},\"InterfaceDefRoute\": %j{InterfaceDefRoute},\"DefRouteGW\": %j{DefRouteGW},\"PrimaryDNSResolver\": %j{PrimaryDNSResolver},\"HostUpTime\": %j{HostUpTime},\"ConnectorUpTime\": %j{ConnectorUpTime},\"NumOfInterfaces\": %d{NumOfInterfaces},\"BytesRxInterface\": %d{BytesRxInterface},\"PacketsRxInterface\": %d{PacketsRxInterface},\"ErrorsRxInterface\": %d{ErrorsRxInterface},\"DiscardsRxInterface\": %d{DiscardsRxInterface},\"BytesTxInterface\": %d{BytesTxInterface},\"PacketsTxInterface\": %d{PacketsTxInterface},\"ErrorsTxInterface\": %d{ErrorsTxInterface},\"DiscardsTxInterface\": %d{DiscardsTxInterface},\"TotalBytesRx\": %d{TotalBytesRx},\"TotalBytesTx\": %d{TotalBytesTx}}\\n"
          source_log_type: "zpn_ast_auth_log"
        connector_groups:
          - id: "11111"
            name: "Test"
      register: lss_controller
    - name: lss_controller
      debug:
        msg: "{{ lss_controller }}"
'''

RETURN = """
# The newly created browser access application segment resource record.
{
            "config": {
                "audit_message": "{\"logType\":\"App Connector Status\",\"tcpPort\":\"20000\",\"appConnectorGroups\":[{\"name\":null,\"id\":\"216196257331292512\"}],\"domainOrIpAddress\":\"10.1.1.1\",\"logStreamContent\":\"{\\\"LogTimestamp\\\": %j{LogTimestamp:time},\\\"Customer\\\": %j{Customer},\\\"SessionID\\\": %j{SessionID},\\\"SessionType\\\": %j{SessionType},\\\"SessionStatus\\\": %j{SessionStatus},\\\"Version\\\": %j{Version},\\\"Platform\\\": %j{Platform},\\\"ZEN\\\": %j{ZEN},\\\"Connector\\\": %j{Connector},\\\"ConnectorGroup\\\": %j{ConnectorGroup},\\\"PrivateIP\\\": %j{PrivateIP},\\\"PublicIP\\\": %j{PublicIP},\\\"Latitude\\\": %f{Latitude},\\\"Longitude\\\": %f{Longitude},\\\"CountryCode\\\": %j{CountryCode},\\\"TimestampAuthentication\\\": %j{TimestampAuthentication:iso8601},\\\"TimestampUnAuthentication\\\": %j{TimestampUnAuthentication:iso8601},\\\"CPUUtilization\\\": %d{CPUUtilization},\\\"MemUtilization\\\": %d{MemUtilization},\\\"ServiceCount\\\": %d{ServiceCount},\\\"InterfaceDefRoute\\\": %j{InterfaceDefRoute},\\\"DefRouteGW\\\": %j{DefRouteGW},\\\"PrimaryDNSResolver\\\": %j{PrimaryDNSResolver},\\\"HostUpTime\\\": %j{HostUpTime},\\\"ConnectorUpTime\\\": %j{ConnectorUpTime},\\\"NumOfInterfaces\\\": %d{NumOfInterfaces},\\\"BytesRxInterface\\\": %d{BytesRxInterface},\\\"PacketsRxInterface\\\": %d{PacketsRxInterface},\\\"ErrorsRxInterface\\\": %d{ErrorsRxInterface},\\\"DiscardsRxInterface\\\": %d{DiscardsRxInterface},\\\"BytesTxInterface\\\": %d{BytesTxInterface},\\\"PacketsTxInterface\\\": %d{PacketsTxInterface},\\\"ErrorsTxInterface\\\": %d{ErrorsTxInterface},\\\"DiscardsTxInterface\\\": %d{DiscardsTxInterface},\\\"TotalBytesRx\\\": %d{TotalBytesRx},\\\"TotalBytesTx\\\": %d{TotalBytesTx}}\\\\n\",\"name\":\"Status\",\"description\":\"status\",\"sessionStatuses\":null,\"enabled\":true,\"useTls\":false,\"policy\":{}}",
                "creation_time": "1643109694",
                "description": "status",
                "enabled": true,
                "format": "{\"LogTimestamp\": %j{LogTimestamp:time},\"Customer\": %j{Customer},\"SessionID\": %j{SessionID},\"SessionType\": %j{SessionType},\"SessionStatus\": %j{SessionStatus},\"Version\": %j{Version},\"Platform\": %j{Platform},\"ZEN\": %j{ZEN},\"Connector\": %j{Connector},\"ConnectorGroup\": %j{ConnectorGroup},\"PrivateIP\": %j{PrivateIP},\"PublicIP\": %j{PublicIP},\"Latitude\": %f{Latitude},\"Longitude\": %f{Longitude},\"CountryCode\": %j{CountryCode},\"TimestampAuthentication\": %j{TimestampAuthentication:iso8601},\"TimestampUnAuthentication\": %j{TimestampUnAuthentication:iso8601},\"CPUUtilization\": %d{CPUUtilization},\"MemUtilization\": %d{MemUtilization},\"ServiceCount\": %d{ServiceCount},\"InterfaceDefRoute\": %j{InterfaceDefRoute},\"DefRouteGW\": %j{DefRouteGW},\"PrimaryDNSResolver\": %j{PrimaryDNSResolver},\"HostUpTime\": %j{HostUpTime},\"ConnectorUpTime\": %j{ConnectorUpTime},\"NumOfInterfaces\": %d{NumOfInterfaces},\"BytesRxInterface\": %d{BytesRxInterface},\"PacketsRxInterface\": %d{PacketsRxInterface},\"ErrorsRxInterface\": %d{ErrorsRxInterface},\"DiscardsRxInterface\": %d{DiscardsRxInterface},\"BytesTxInterface\": %d{BytesTxInterface},\"PacketsTxInterface\": %d{PacketsTxInterface},\"ErrorsTxInterface\": %d{ErrorsTxInterface},\"DiscardsTxInterface\": %d{DiscardsTxInterface},\"TotalBytesRx\": %d{TotalBytesRx},\"TotalBytesTx\": %d{TotalBytesTx}}\\n",
                "id": "216196257331292567",
                "lss_host": "10.1.1.1",
                "lss_port": "20000",
                "modified_by": "216196257331282070",
                "name": "Status",
                "source_log_type": "zpn_ast_auth_log",
                "use_tls": false
            },
            "connector_groups": [
                {
                    "city_country": "Langley, CA",
                    "country_code": "CA",
                    "creation_time": "1642798564",
                    "description": "USA App Connector Group",
                    "dns_query_type": "IPV4",
                    "enabled": true,
                    "id": "216196257331292512",
                    "latitude": "49.1041779",
                    "location": "Langley City, BC, Canada",
                    "longitude": "-122.6603519",
                    "lss_app_connector_group": false,
                    "modified_by": "216196257331282070",
                    "name": "USA App Connector Group",
                    "override_version_profile": true,
                    "upgrade_day": "SUNDAY",
                    "upgrade_time_in_secs": "66600",
                    "version_profile_id": "2",
                    "version_profile_name": "New Release",
                    "version_profile_visibility_scope": "ALL"
                }
            ],
            "id": "216196257331292567"
        }
"""

def core(module):
    state = module.params.get("state", None)
    customer_id = module.params.get("customer_id", None)
    service = LSSConfigControllerService(module, customer_id)
    lss_config = dict()
    params = [
        "id",
        "config",
        "connector_groups",
        "policy_rule_resource"
    ]
    for param_name in params:
        lss_config[param_name] = module.params.get(param_name, None)
    existing_lss_config = service.getByIDOrName(
        lss_config.get("id"), lss_config.get("config", {}).get("name"))
    if state == "present":
        if existing_lss_config is not None:
            """Update"""
            existing_lss_config = service.update(existing_lss_config)
            module.exit_json(changed=True, data=existing_lss_config)
        else:
            """Create"""
            lss_config = service.create(lss_config)
            module.exit_json(changed=False, data=lss_config)
    elif state == "absent":
        if existing_lss_config is not None:
            service.delete(existing_lss_config.get("id"))
            module.exit_json(changed=False, data=existing_lss_config)
    module.exit_json(changed=False, data={})


def main():
    """Main"""
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    id_name_spec = dict(type='list', elements='dict', options=dict(id=dict(
        type='str', required=True), name=dict(type='str', required=False)), required=False)
    argument_spec.update(
        id=dict(type='str'),
        policy_rule_resource=dict(
            type='dict',
            options=dict(
                priority=dict(
                    type='str', required=False
                ),
                reauth_idle_timeout=dict(
                    type='str', required=False
                ),
                policy_type=dict(
                    type='str', required=False
                ),
                reauth_default_rule=dict(
                    type='bool', required=False
                ),
                custom_msg=dict(
                    type='str', required=False
                ),
                action_id=dict(
                    type='str', required=False
                ),
                operator=dict(
                    type='str', required=False
                ),
                bypass_default_rule=dict(
                    type='bool', required=False
                ),
                policy_set_id=dict(
                    type='str', required=False
                ),
                default_rule=dict(
                    type='bool', required=False
                ),
                action=dict(
                    type='str', required=False
                ),
                conditions=dict(
                    type='list',
                    elements='dict',
                    options=dict(
                        negated=dict(type='bool', required=False),
                        operator=dict(type='str', required=True),
                        operands=dict(
                            type='list',
                            elements='dict',
                            options=dict(
                                values=dict(
                                    type='list', elements='str', required=False
                                ),
                                object_type=dict(
                                    type='str', required=True, choices=["APP", "APP_GROUP", "CLIENT_TYPE"]
                                ),
                            ),
                            required=False
                        ),
                    ), required=False),
                name=dict(type='str', required=True),
                reauth_timeout=dict(type='str', required=False),
                rule_order=dict(type='str', required=False),
                description=dict(type='str', required=False),
                id=dict(type='str'),
                lss_default_rule=dict(type='bool', required=False),
            ),
            required=False
        ),
        connector_groups=id_name_spec,
        config=dict(
            type='dict',
            options=dict(
                format=dict(type='str', required=True),
                id=dict(type='str'),
                name=dict(type='str', required=True),
                lss_port=dict(type='str', required=True),
                use_tls=dict(type='bool', required=False, default=False),
                enabled=dict(type='bool', required=False, default=True),
                description=dict(type='str', required=False),
                filter=dict(type='list', elements='str', required=False),
                lss_host=dict(type='str', required=True),
                source_log_type=dict(type='str', required=True, choices=["zpn_trans_log", "zpn_auth_log", "zpn_ast_auth_log",
                                     "zpn_http_trans_log", "zpn_audit_log", "zpn_sys_auth_log", "zpn_http_insp", "zpn_ast_comprehensive_stats", ]),
                audit_message=dict(type='str', required=False),
            ),
            required=False
        ),
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
