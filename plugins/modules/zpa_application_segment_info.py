#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_application_segment_info
short_description: Retrieve an application segment information.
description:
    - This module will allow the retrieval of information about an application segment.
author: "William Guilherme (@willguibr)"
version_added: "1.0.0"
options:
  client_id:
    description: ""
    required: false
    type: str
  client_secret:
    description: ""
    required: false
    type: str
  customer_id:
    description: ""
    required: false
    type: str
  name:
    description: "Name of the application segment."
    required: false
    type: str
  id:
    description: "ID of the application segment."
    required: False
    type: str
"""

EXAMPLES = """
- name: Retrieve Details of All Application Segments
  willguibr.zpacloud.zpa_application_segment_info:

- name: Retrieve Details of a Specific Application Segments by Name
  willguibr.zpacloud.zpa_application_segment_info:
    name: "Example Application Segment"

- name: Retrieve Details of a Specific Application Segments by ID
  willguibr.zpacloud.zpa_application_segment_info:
    id: "216196257331291981"
"""

RETURN = """
# Returns information on a specified Application Segment.
"""

from re import T
from traceback import format_exc

from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_application_segment import (
    ApplicationSegmentService,
)
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper,
)


def core(module):
    app_name = module.params.get("name", None)
    app_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = ApplicationSegmentService(module, customer_id, ZPAClientHelper(module))
    apps = []
    if app_id is not None:
        app = service.getByID(app_id)
        if app is None:
            module.fail_json(
                msg="Failed to retrieve application segment ID: '%s'" % (id)
            )
        apps = [app]
    elif app_name is not None:
        app = service.getByName(app_name)
        if app is None:
            module.fail_json(
                msg="Failed to retrieve application segment Name: '%s'" % (app_name)
            )
        apps = [app]
    else:
        apps = service.getAll()
    module.exit_json(changed=False, data=apps)


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    argument_spec.update(
        name=dict(type="str", required=False),
        id=dict(type="str", required=False),
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
