#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_browser_access import BrowserAccessService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_browser_access
short_description: Create a Browser Access Application Segment.
description:
  - This module create/update/delete a Browser Access Application Segment in the ZPA Cloud.
author:
  - William Guilherme (@willguibr)
version_added: "1.0.0"
options:
  default_max_age:
    type: str
    required: False
    default: ""
    description: "default_max_age"
  ip_anchored:
    type: bool
    required: False
    description: "ip_anchored"
  udp_port_range:
    type: list
    elements: dict
    required: False
    description: "udp port range"
  id:
    type: str
    description: "Unique ID."
  double_encrypt:
    type: bool
    required: False
    description: "Whether Double Encryption is enabled or disabled for the app."
  icmp_access_type:
    type: str
    required: False
    default: "NONE"
    choices: ["PING_TRACEROUTING", "PING", "NONE"]
    description: "icmp access type."
  default_idle_timeout:
    type: str
    required: False
    default: ""
    description: "default idle timeout."
  modifiedby:
    type: str
    required: False
    description: "modified by."
  passive_health_enabled:
    type: bool
    required: False
    description: "passive health enabled."
  bypass_type:
    type: str
    required: False
    description: "Indicates whether users can bypass ZPA to access applications."
    choices: ["ALWAYS", "NEVER", "ON_NET"]
  is_cname_enabled:
    type: bool
    required: False
    description: "Indicates if the Zscaler Client Connector (formerly Zscaler App or Z App) receives CNAME DNS records from the connectors."
  name:
    type: str
    required: True
    description: "Name of the application."
  config_space:
    type: str
    required: False
    default: "DEFAULT"
    choices: ["DEFAULT", "SIEM"]
    description: "config space."
  health_reporting:
    type: str
    required: False
    description: "Whether health reporting for the app is Continuous or On Access. Supported values: NONE, ON_ACCESS, CONTINUOUS."
    default: "NONE"
    choices: ["NONE", "ON_ACCESS", "CONTINUOUS"]
  log_features:
    type: str
    required: False
    choices: ["skip_discovery", "full_wildcard"]
    description: "log features."
  server_groups:
    type: list
    elements: str
    required: True
    description: "List of the server group IDs."
  segment_group_id:
    type: str
    required: True
    description: "segment group id."
  description:
    type: str
    required: False
    description: "Description of the application."
  health_check_type:
    type: str
    description: "health check type."
  segment_group_name:
    type: str
    required: False
    description: "segment group name."
  tcp_port_range:
    type: list
    elements: dict
    required: False
    description: "tcp port range"
  udp_port_ranges:
    type: list
    elements: str
    required: False
    description: "UDP port ranges used to access the app."
  tcp_port_ranges:
    type: list
    elements: str
    required: False
    description: "TCP port ranges used to access the app."
  enabled:
    type: bool
    required: False
    description: "Whether this application is enabled or not."
  domain_names:
    type: list
    elements: str
    required: True
    description: "List of domains and IPs."
  clientless_apps:
    type: list
    elements: dict
    required: False
    description: ""
"""

EXAMPLES = """
- name: Create an app segment
  willguibr.zpacloud.zpa_browser_access:
    name: Example Application
    description: Example Application Test
    enabled: true
    health_reporting: ON_ACCESS
    bypass_type: NEVER
    clientless_apps:
      - name: "crm.example.com"
        application_protocol: "HTTP"
        application_port: "8080"
        certificate_id: "216196257331282583"
        trust_untrusted_cert: true
        enabled: true
        domain: "crm.example.com"
      - name: "crm2.example.com"
        application_protocol: "HTTP"
        application_port: "8082"
        certificate_id: "216196257331282583"
        trust_untrusted_cert: true
        enabled: true
        domain: "crm.example.com"
    is_cname_enabled: true
    tcp_port_range:
      - from: "80"
        to: "80"
    domain_names:
      - crm.example.com
    segment_group_id: "216196257331291896"
    server_groups:
      - "216196257331291969"
"""

RETURN = """
# The newly created browser access application segment resource record.
"""


def core(module):
    state = module.params.get("state", None)
    customer_id = module.params.get("customer_id", None)
    service = BrowserAccessService(module, customer_id)
    app = dict()
    params = [
        "segment_group_id",
        "segment_group_name",
        "bypass_type",
        "clientless_apps",
        "config_space",
        "creation_time",
        "default_idle_timeout",
        "default_max_age",
        "description",
        "domain_names",
        "double_encrypt",
        "enabled",
        "health_check_type",
        "health_reporting",
        "icmp_access_type",
        "id",
        "ip_anchored",
        "is_cname_enabled",
        "modifiedby",
        "modified_time",
        "name",
        "passive_health_enabled",
        "tcp_port_range",
        "udp_port_range",
        "server_groups",


    ]
    for param_name in params:
        app[param_name] = module.params.get(param_name)
    existing_app = service.getByIDOrName(app.get("id"), app.get("name"))
    if existing_app is not None:
        id = existing_app.get("id")
        existing_app.update(app)
        existing_app["id"] = id
    if state == "present":
        if existing_app is not None:
            """Update"""
            existing_app = service.update(existing_app)
            module.exit_json(changed=True, data=existing_app)
        else:
            """Create"""
            app = service.create(app)
            module.exit_json(changed=False, data=app)
    elif state == "absent":
        if existing_app is not None:
            # first detach it from the segment group
            service.detach_from_segment_group(existing_app.get(
                "id"), existing_app.get("segment_group_id"))
            service.delete(existing_app.get("id"))
            module.exit_json(changed=False, data=existing_app)
    module.exit_json(changed=False, data={})


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    port_spec = dict(to=dict(type='str', required=False))
    port_spec["from"] = dict(type='str', required=False)
    id_name_spec = dict(type='list', elements='dict', options=dict(id=dict(
        type='str', required=True), name=dict(type='str', required=False)), required=True)
    argument_spec.update(
        tcp_port_range=dict(type='list', elements='dict',
                            options=port_spec, required=False),
        enabled=dict(type='bool', required=False),
        default_idle_timeout=dict(type='str', required=False, default=""),
        bypass_type=dict(type='str', required=False),
        udp_port_range=dict(type='list', elements='dict',
                            options=port_spec, required=False),
        config_space=dict(type='str', required=False,
                          default="DEFAULT", choices=["DEFAULT", "SIEM"]),
        health_reporting=dict(type='str', required=False,
                              default="NONE", choices=["NONE", "ON_ACCESS", "CONTINUOUS"]),
        segment_group_id=dict(type='str', required=True),
        double_encrypt=dict(type='bool', required=False),
        health_check_type=dict(type='str'),
        default_max_age=dict(type='str', required=False, default=""),
        is_cname_enabled=dict(type='bool', required=False),
        passive_health_enabled=dict(type='bool', required=False),
        ip_anchored=dict(type='bool', required=False),
        name=dict(type='str', required=True),
        description=dict(type='str', required=False),
        icmp_access_type=dict(type='str', required=False,
                              default="NONE", choices=["PING_TRACEROUTING", "PING", "NONE"]),
        creation_time=dict(type='str', required=False),
        modifiedby=dict(type='str', required=False),
        modified_time=dict(type='str', required=False),
        id=dict(type='str'),
        server_groups=id_name_spec,
        segment_group_name=dict(type='str', required=False),
        domain_names=dict(type='list', elements='str', required=True),
        clientless_apps=dict(
            type='list',
            elements='dict',
            options=dict(
                path=dict(type='str', required=False),
                trust_untrusted_cert=dict(type='bool', required=False),
                allow_options=dict(type='bool', required=False),
                description=dict(type='str', required=False),
                id=dict(type='str'),
                cname=dict(type='str', required=False),
                hidden=dict(type='bool', required=False),
                app_id=dict(type='str'),
                application_port=dict(type='str', required=False),
                application_protocol=dict(type='str', required=True),
                name=dict(type='str', required=True),
                certificate_id=dict(type='str', required=True),
                certificate_name=dict(type='str', required=False),
                domain=dict(type='str', required=False),
                enabled=dict(type='bool', required=False),
                local_domain=dict(type='str', required=False),
            ),
            required=False
        ),
        state=dict(type="str", choices=[
                   "present", "absent"], default="present")
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
