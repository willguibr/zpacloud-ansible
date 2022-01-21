#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_provisioning_key import ProvisioningKeyService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_provisioning_key_info
short_description: Retrieves details about a Provisioning Key.
description:
  - This module will allow the retrieval of information abouta Provisioning Key by association type (CONNECTOR_GRP or SERVICE_EDGE_GRP).
author: William Guilherme (@willguibr)
version_added: "1.0.0"
requirements:
  - supported starting from zpa_api >= 1.0
options:
  name:
    description:
      - Name of the provisioning key.
    required: false
    type: str
  id:
    description:
      - ID of the provisioning key.
    required: false
    type: str
  association_type:
    type: str
    required: true
    description: "Specifies the provisioning key type for App Connectors or ZPA Private Service Edges. The supported values are CONNECTOR_GRP and SERVICE_EDGE_GRP."
"""

EXAMPLES = """
- name: Gather Details of All SERVICE_EDGE_GRP Provisioning Keys
  willguibr.zpacloud.zpa_provisioning_key_info:
    association_type: "SERVICE_EDGE_GRP"

- name: Gather Details of All SERVICE_EDGE_GRP Provisioning Keys by Name
  willguibr.zpacloud.zpa_provisioning_key_info:
    name: "Example Service Edge Group"
    association_type: "SERVICE_EDGE_GRP"

- name: Gather Details of All SERVICE_EDGE_GRP Provisioning Keys by ID
  willguibr.zpacloud.zpa_provisioning_key_info:
    id: "8691"
    association_type: "SERVICE_EDGE_GRP"
"""

RETURN = """
# Returns information on a specified provisioning key resource.
"""

def core(module):
    provisioning_key_name = module.params.get("name", None)
    provisioning_key_id = module.params.get("id", None)
    association_type = module.params.get("association_type", None)
    customer_id = module.params.get("customer_id", None)
    service = ProvisioningKeyService(module, customer_id)
    provisioning_keys = []
    if provisioning_key_id is not None:
        provisioning_key = service.getByID(
            provisioning_key_id, association_type)
        if provisioning_key is None:
            module.fail_json(
                msg="Failed to retrieve Provisioning Key ID: '%s'" % (id))
        provisioning_keys = [provisioning_key]
    elif provisioning_key_name is not None:
        provisioning_key = service.getByName(
            provisioning_key_name, association_type)
        if provisioning_key is None:
            module.fail_json(
                msg="Failed to retrieve Provisioning Key Name: '%s'" % (provisioning_key_name))
        provisioning_keys = [provisioning_key]
    else:
        provisioning_keys = service.getAll(association_type)
    module.exit_json(changed=False, data=provisioning_keys)


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    argument_spec.update(
        name=dict(type="str", required=False),
        id=dict(type="str", required=False),
        association_type=dict(type="str", choices=[
                              "CONNECTOR_GRP", "SERVICE_EDGE_GRP"], required=True),
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
