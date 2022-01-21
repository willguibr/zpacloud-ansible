#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_application_segment import ApplicationSegmentService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_application_segment
short_description: Create an application segment in the ZPA Cloud.
description:
    - This module will create/update/delete an application segment
author:
    - William Guilherme (@willguibr)
version_added: "1.0.0"
options:
  name:
    description: 
      - Name of the application.
    required: true
    type: str
  description:
    description:
      - Description of the application.
    required: false
    type: str
  default_max_age:
    description:
      - default_max_age
    required: false
    type: str
  ip_anchored:
    description:
      - Whether Source IP Anchoring for use with ZIA, is enabled or disabled for the app.
    type: bool
    required: false
  tcp_port_range:
    type: list
    elements: dict
    description:
      - List of tcp port range pairs, e.g. [22, 22] for port 22-22, [80, 100] for 80-100.
    required: true
    suboptions:
      from:
        type: str
        required: false
        description:
          - List of valid TCP ports. The application segment API supports multiple TCP and UDP port ranges.
      to:
        type: str
        required: false
        description:
          - List of valid TCP ports. The application segment API supports multiple TCP and UDP port ranges.
  udp_port_range:
    type: list
    elements: dict
    description:
      - List of udp port range pairs, e.g. [‘35000’, ‘35000’] for port 35000.
    required: true
    suboptions:
      from:
        type: str
        required: false
        description:
          - List of valid UDP ports. The application segment API supports multiple TCP and UDP port ranges.
      to:
        type: str
        required: false
        description:
          - List of valid UDP ports. The application segment API supports multiple TCP and UDP port ranges.
  double_encrypt:
    description:
      - Whether Double Encryption is enabled or disabled for the app.
    type: bool
    required: false
  icmp_access_type:
    description:
      - icmp access type.
    type: str
    required: false
    choices:
      - PING_TRACEROUTING
      - PING
      - NONE
    default: NONE
  default_idle_timeout:
    description:
      - default idle timeout.
    type: str
    required: false
  passive_health_enabled:
    description:
      - passive health enabled.
    type: bool
    required: false
  bypass_type:
    description:
      - Indicates whether users can bypass ZPA to access applications.
    type: str
    required: false
    choices:
      - ALWAYS
      - NEVER
      - ON_NET
    default: NEVER
  is_cname_enabled:
    description:
      - Indicates if the Zscaler Client Connector (formerly Zscaler App or Z App) receives CNAME DNS records from the connectors.
    type: bool
    required: false 
  config_space:
    description:
      - config space.
    type: str
    required: false
    choices:
      - DEFAULT
      - SIEM
    default: DEFAULT
  health_reporting:
    description:
      - Whether health reporting for the app is Continuous or On Access. Supported values are NONE, ON_ACCESS, CONTINUOUS
    type: str
    required: false
    choices:
      - NONE
      - ON_ACCESS
      - CONTINUOUS
    default: NONE
  log_features:
    description:
      - log features.
    type: str
    required: false
    choices:
      - skip_discovery
      - full_wildcard
  server_groups:
    description:
      - ID of the server group.
    type: list
    elements: dict
    required: true
    suboptions:
      id:
        type: str
        required: true
        description:
          - ID of the server group.
  segment_group_id:
    description:
      - ID of the segment group.
    type: str
    required: true
  segment_group_name:
    description:
      - segment group name.
    type: str
    required: false
  health_check_type:
    description:
      - health check type.
    type: str
    required: false
  enabled:
    description:
      - Whether this application is enabled or not.
    type: bool
    required: false
  domain_names:
    description:
      - List of domains and IPs.
    type: list
    elements: str
    required: true
"""

EXAMPLES = """
- name: Create/Update/Delete an application segment.
  willguibr.zpacloud.zpa_application_segment:
    name: Example Application Segment
    description: Example Application Segment
    enabled: true
    health_reporting: ON_ACCESS
    bypass_type: NEVER
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
# The newly created application segment resource record.
"""


def core(module):
    state = module.params.get("state", None)
    customer_id = module.params.get("customer_id", None)
    service = ApplicationSegmentService(module, customer_id)
    app = dict()
    params = [
        "tcp_port_range",
        "enabled",
        "default_idle_timeout",
        "bypass_type",
        "udp_port_range",
        "config_space",
        "health_reporting",
        "segment_group_id",
        "double_encrypt",
        "health_check_type",
        "default_max_age",
        "is_cname_enabled",
        "passive_health_enabled",
        "ip_anchored",
        "name",
        "description",
        "icmp_access_type",
        "creation_time",
        "modifiedby",
        "modified_time",
        "id",
        "server_groups",
        "segment_group_name",
        "domain_names",
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
            app = service.update(existing_app)
            module.exit_json(changed=True, data=app)
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
