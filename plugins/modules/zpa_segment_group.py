#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_segment_group import SegmentGroupService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_segment_group
short_description: Create a Segment Group
description:
    - This module will create/update/delete a segment group resource.
author:
    - William Guilherme (@willguibr)
version_added: '1.0.0'
options:
  name:
    description:
        - Name of the server group.
    required: false
    type: str
  id:
    description:
        - ID of the server group.
    required: false
    type: str
  config_space:
    description:
        - ID of the server group.
    type: str
    choices:
        - SIEM
        - DEFAULT
    default: DEFAULT               
"""

EXAMPLES = """
- name: Create/Update/Delete a Segment Group
    willguibr.zpacloud.zpa_segment_group:
        name: Example Segment Group
        config_space: "DEFAULT"
        description: Example Segment Group
        enabled: true
        policy_migrated: true
        tcp_keep_alive_enabled: "1"
"""

RETURN = """
# The newly created segment group resource record.
"""

def core(module):
    state = module.params.get("state", None)
    customer_id = module.params.get("customer_id", None)
    service = SegmentGroupService(module, customer_id)
    segment_group = dict()
    params = [
        "applications",
        "config_space",
        "description",
        "enabled",
        "id",
        "name",
        "policy_migrated",
        "tcp_keep_alive_enabled",
    ]
    for param_name in params:
        segment_group[param_name] = module.params.get(param_name, None)
    existing_segment_group = service.getByIDOrName(
        segment_group.get("id"), segment_group.get("name"))
    if existing_segment_group is not None:
        id = existing_segment_group.get("id")
        existing_segment_group.update(segment_group)
        existing_segment_group["id"] = id
    if state == "present":
        if existing_segment_group is not None:
            """Update"""
            segment_group = service.update(existing_segment_group)
            module.exit_json(changed=True, data=segment_group)
        else:
            """Create"""
            segment_group = service.create(segment_group)
            module.exit_json(changed=False, data=segment_group)
    elif state == "absent":
        if existing_segment_group is not None:
            service.delete(existing_segment_group.get("id"))
            module.exit_json(changed=False, data=existing_segment_group)
    module.exit_json(changed=False, data={})


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    argument_spec.update(
        applications=dict(type='list', elements='dict', options=dict(id=dict(
            type='str', required=True), name=dict(type='str', required=False)), required=False),
        config_space=dict(type='str', required=False,
                          default="DEFAULT", choices=["DEFAULT", "SIEM"]),
        description=dict(type='str', required=False),
        enabled=dict(type='bool', required=False),
        id=dict(type='str'),
        name=dict(type='str', required=True),
        policy_migrated=dict(type='bool', required=False),
        tcp_keep_alive_enabled=dict(type='str', required=False),
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
