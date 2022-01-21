#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_cloud_connector_group import CloudConnectorGroupService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_cloud_connector_group_info
short_description: Retrieves cloud connector group information.
description:
  - This module will allow the retrieval of information about a cloud connector group.
author:
  - William Guilherme (@willguibr)
version_added: "1.0.0"
options:
  name:
    description:
      - Name of the Cloud Connector Group.
    required: false
    type: str
  id:
    description:
      - ID of the Cloud Connector Group.
    required: false
    type: str
"""

EXAMPLES = """
- name: Get Information Details of All Cloud Connector Groups
  willguibr.zpacloud.zpa_cloud_connector_group_info:

- name: Get Information Details of a Cloud Connector Group by Name
  willguibr.zpacloud.zpa_cloud_connector_group_info:
    name: zs-cc-vpc-096108eb5d9e68d71-ca-central-1a

- name: Get Information Details of a Cloud Connector Group by ID
  willguibr.zpacloud.zpa_cloud_connector_group_info:
    id: "216196257331292017"  
"""

RETURN = """
# Returns information on a specified Cloud Connector Group.
"""

def core(module):
    cloud_connector_name = module.params.get("name", None)
    cloud_connector_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = CloudConnectorGroupService(module, customer_id)
    connectors = []
    if cloud_connector_id is not None:
        connector = service.getByID(cloud_connector_id)
        if connector is None:
            module.fail_json(
                msg="Failed to retrieve App Connector Group ID: '%s'" % (id))
        connectors = [connector]
    elif cloud_connector_name is not None:
        connector = service.getByName(cloud_connector_name)
        if connector is None:
            module.fail_json(
                msg="Failed to retrieve App Connector Group Name: '%s'" % (cloud_connector_name))
        connectors = [connector]
    else:
        connectors = service.getAll()
    module.exit_json(changed=False, data=connectors)


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
