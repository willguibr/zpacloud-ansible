#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_service_edge_groups import ServiceEdgeGroupService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_service_edge_groups_info
short_description: Retrieves information about a Service Edge Group.
description:
    - This module will allow the retrieval of information about a Service Edge Group resource.
author:
  - William Guilherme (@willguibr)
version_added: "1.0.0"
options:
  name:
    description:
      - Name of the Service Edge Group..
    required: false
    type: str
  id:
    description:
      - ID of the Service Edge Group..
    required: false
    type: str

"""

EXAMPLES = """
- name: Get information about all Service Edge Groups
  willguibr.zpacloud.zpa_service_edge_groups_info:
    
- name: Get information about Service Edge Connector Group by ID
  willguibr.zpacloud.zpa_service_edge_groups_info:
    id: "198288282"

- name: Get information about Service Edge Connector Group by Name
  willguibr.zpacloud.zpa_service_edge_groups_info:
    name: "Example"
"""

RETURN = """
# Returns information on a specified Service Edge Group.
"""


def core(module):
    service_edge_name = module.params.get("name", None)
    service_edge_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = ServiceEdgeGroupService(module, customer_id)
    service_edges = []
    if service_edge_id is not None:
        service_edge = service.getByID(service_edge_id)
        if service_edge is None:
            module.fail_json(
                msg="Failed to retrieve Service Edge Group ID: '%s'" % (id))
        service_edges = [service_edge]
    elif service_edge_name is not None:
        service_edge = service.getByName(service_edge_name)
        if service_edge is None:
            module.fail_json(
                msg="Failed to retrieve Service Edge Group Name: '%s'" % (service_edge_name))
        service_edges = [service_edge]
    else:
        service_edges = service.getAll()
    module.exit_json(changed=False, data=service_edges)


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
