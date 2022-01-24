#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_app_connector_controller import AppConnectorControllerService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_app_connector_controller
short_description: Manages an app connector controller
description:
  - This module update/delete/bulk delete App Connector Controllers in the ZPA Cloud.
author:
  - William Guilherme (@willguibr)
version_added: "1.0.0"
options:
  application_start_time:
    description:
      - "".
    required: false
    type: str
  app_connector_group_id:
    description:
      - "".
    required: false
    type: str
  app_connector_group_name:
    description:
        - "".
    type: str
  control_channel_status:
    description:
      - Read only.Ignored in PUT/POST calls. Expected values: UNKNOWN/ZPN_STATUS_AUTHENTICATED(1)/ZPN_STATUS_DISCONNECTED.
    type: str
    choices:
      - UNKNOWN
      - ZPN_STATUS_AUTHENTICATED
      - FAILED
      - ZPN_STATUS_DISCONNECTED
  creation_time:
    description:
      - "".
    type: str
  ctrl_broker_name:
    description:
      - Read only. Ignored in PUT/POST calls.
    type: str 
  current_version:
    description:
      - Read only. Ignored in PUT/POST calls.
    type: str
  description:
    description:
      - Description of the App Connector.
    type: str
  enabled:
    description:
      - Whether the App Connector is enabled or not.
    type: bool
  expected_upgrade_time:
    description:
      - Read only. Ignored in PUT/POST calls.
    type: str
  expected_version:
    description:
      - Read only. Ignored in PUT/POST calls.
    type: str
  fingerprint:
    description:
      - "".
    type: str
  id:
    description:
      - "".
    type: str
  ip_acl:
    description:
      - "".
    type: str
  issued_cert_id:
    description:
      - "".
    type: str
  last_broker_connect_time:
    description:
      - Read only. Ignored in PUT/POST calls.
    type: str
  last_broker_connect_time_duration:
    description:
      - Read only. Ignored in PUT/POST calls.
    type: str      
  last_broker_disconnect_time:
    description:
      - Read only. Ignored in PUT/POST calls.
    type: str
  last_broker_disconnect_time_duration:
    description:
      - Read only. Ignored in PUT/POST calls.
    type: str
  last_upgrade_time:
    description:
      - Read only. Ignored in PUT/POST calls.
    type: str
  latitude:
    description:
      - Latitude of the App Connector Controller. Integer or decimal. With values in the range of -90 to 90.
    required: true
    type: str
  location:
    description:
      - Location of the App Connector Controller.
    required: true
    type: str
  longitude:
    description:
      - Longitude of the App Connector Controller. Integer or decimal. With values in the range of -180 to 180.
    required: true
    type: str
  modified_by:
    description:
      - "".
    required: false
    type: str
  modified_time:
    description:
      - "".
    required: false
    type: str
  name:
    description:
      - "".
    required: false
    type: str
  provisioning_key_id:
    description:
      - "".
    required: false
    type: str
  provisioning_key_name:
    description:
      - "".
    required: false
    type: str
  platform:
    description:
      - "".
    required: false
    type: str
  previous_version:
    description:
      - "".
    required: false
    type: str
  private_ip:
    description:
      - "".
    required: false
    type: str
  public_ip:
    description:
      - "".
    required: false
    type: str
  sarge_version:
    description:
      - "".
    required: false
    type: str
  enrollment_cert:
    description:
      - "".
    required: false
    type: str
  upgrade_attempt:
    description:
      - "".
    required: false
    type: str
  upgrade_status:
    description:
      - Read only. Ignored in PUT/POST calls..
    required: false
    type: str
    choices:
      - COMPLETE
      - IN_PROGRESS
      - FAILED
      - UNKNOWN
      - RESTARTING
  state:
    description:
      - Whether the app connector group should be present or absent.
    type: str
    choices:
        - present
        - absent
    default: present
"""

EXAMPLES = """
- name: Create/Update/Delete an App Connector Group
  willguibr.zpacloud.zpa_app_connector_groups:
    name: "Example"
    description: "Example2"
    enabled: true
    city_country: "California, US"
    country_code: "US"
    latitude: "37.3382082"
    longitude: "-121.8863286"
    location: "San Jose, CA, USA"
    upgrade_day: "SUNDAY"
    upgrade_time_in_secs: "66600"
    override_version_profile: true
    version_profile_id: "0"
    dns_query_type: "IPV4"
"""

RETURN = """
# The newly created app connector group resource record.
"""


def core(module):
    state = module.params.get("state", None)
    customer_id = module.params.get("customer_id", None)
    service = AppConnectorControllerService(module, customer_id)
    app = dict()
    params = [
        "application_start_time",
        "app_connector_group_id",
        "app_connector_group_name",
        "control_channel_status",
        "creation_time",
        "ctrl_broker_name",
        "current_version",
        "description",
        "enabled",
        "expected_upgrade_time",
        "expected_version",
        "fingerprint",
        "id",
        "ip_acl",
        "issued_cert_id",
        "last_broker_connect_time",
        "last_broker_connect_time_duration",
        "last_broker_disconnect_time",
        "last_broker_disconnect_time_duration",
        "last_upgrade_time",
        "latitude",
        "location",
        "longitude",
        "modified_by",
        "modified_time",
        "name",
        "provisioning_key_id",
        "provisioning_key_name",
        "platform",
        "previous_version",
        "private_ip",
        "public_ip",
        "sarge_version",
        "enrollment_cert",
        "upgrade_attempt",
        "upgrade_status",
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
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    # id_name_spec = dict(type='list', elements='dict', options=dict(id=dict(
    #     type='str', required=False), name=dict(type='str', required=False)), required=False)
    argument_spec.update(
        # connectors=id_name_spec,
        application_start_time=dict(type="str", required=False),
        app_connector_group_id=dict(type="str", required=False),
        app_connector_group_name=dict(type="str", required=False),
        control_channel_status=dict(type="str", required=False),
        creation_time=dict(type="str", required=False),
        ctrl_broker_name=dict(type="str", required=False),
        current_version=dict(type="str", required=False),   
        description=dict(type="str", required=False),          
        enabled=dict(type="bool", default=True, required=False),
        expected_upgrade_time=dict(type="str", required=False),   
        expected_version=dict(type="str", required=False),
        fingerprint=dict(type="str", required=False),
        id=dict(type="str", required=False),
        ip_acl=dict(type="str", required=False),
        issued_cert_id=dict(type="str", required=False),
        last_broker_connect_time=dict(type="str", required=False),
        last_broker_connect_time_duration=dict(type="str", required=False),
        last_broker_disconnect_time=dict(type="str", required=False),
        last_broker_disconnect_time_duration=dict(type="str", required=False), 
        last_upgrade_time=dict(type="str", required=False), 
        latitude=dict(type="str", required=False),   
        location=dict(type="str", required=False),
        longitude=dict(type="str", required=False),        
        modified_by=dict(type="str", required=False),                
        modified_time=dict(type="str", required=False),
        name=dict(type="str", required=False),
        provisioning_key_id=dict(type="str", required=False),
        provisioning_key_name=dict(type="str", required=False),
        platform=dict(type="str", required=False),
        previous_version=dict(type="str", required=False),                                                             
        private_ip=dict(type="str", required=False),
        public_ip=dict(type="str", required=False),
        sarge_version=dict(type="str", required=False),
        enrollment_cert=dict(type="str", required=False),
        upgrade_attempt=dict(type="str", required=False),
        upgrade_status=dict(type="str", required=False),
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
