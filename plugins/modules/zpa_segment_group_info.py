#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_segment_group import SegmentGroupService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_segment_group_info
short_description: Retrieves information about a segment group.
description:
    - This module will allow the retrieval of information about a segment group.
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
"""

EXAMPLES = """
- name: Get Detail Information of All Segment Groups
    willguibr.zpacloud.zpa_segment_group_info:

- name: Get Details of a Segment Group by Name
    willguibr.zpacloud.zpa_segment_group_info:
    name: "Example"

- name: Get Details of a Segment Group by ID
    willguibr.zpacloud.zpa_segment_group_info:
    id: "216196257331291969"
"""

RETURN = """
# Returns information on a specified segment group.
"""


def core(module):
    segment_group_name = module.params.get("name", None)
    segment_group_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = SegmentGroupService(module, customer_id)
    segment_groups = []
    if segment_group_id is not None:
        segment_group = service.getByID(segment_group_id)
        if segment_group is None:
            module.fail_json(
                msg="Failed to retrieve segment group ID: '%s'" % (id))
        segment_groups = [segment_group]
    elif segment_group_name is not None:
        segment_group = service.getByName(segment_group_name)
        if segment_group is None:
            module.fail_json(
                msg="Failed to retrieve segment group Name: '%s'" % (segment_group_name))
        segment_groups = [segment_group]
    else:
        segment_groups = service.getAll()
    module.exit_json(changed=False, data=segment_groups)


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
