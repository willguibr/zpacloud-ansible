#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_scim_group import ScimGroupService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_scim_group_info
short_description: Retrieves scim group information from a given IDP
description:
  - This module will allow the retrieval of information about scim group(s) from a given IDP
author: William Guilherme (@willguibr)
version_added: "1.0.0"
requirements:
  - supported starting from zpa_api >= 1.0
options:
  name:
    description:
      - Name of the scim group.
    required: false
    type: str
  idp_name:
    description:
      - Name of the IDP.
    required: true
    type: str
  id:
    description:
      - ID of the scim group.
    required: false
    type: str
"""

EXAMPLES = """
- name: Get Information About All SCIM Groups from an IdP
  willguibr.zpacloud.zpa_scim_attribute_header_info:
    idp_name: "IdP_Name"
    
- name: Get Information About a SCIM Group by ID
  willguibr.zpacloud.zpa_scim_attribute_header_info:
    id: 216196257331285827
    idp_name: "IdP_Name"
    
- name: Get Information About a SCIM Group by Name 
  willguibr.zpacloud.zpa_scim_attribute_header_info:
    name: "Finance"
    idp_name: "IdP_Name"
"""

RETURN = """
# Returns information on a specified posture profile.
"""


def core(module):
    scim_name = module.params.get("name", None)
    scim_id = module.params.get("id", None)
    idp_name = module.params.get("idp_name", None)
    customer_id = module.params.get("customer_id", None)
    service = ScimGroupService(module, customer_id)
    attributes = []
    if scim_id is not None:
        attribute = service.getByID(scim_id)
        if attribute is None:
            module.fail_json(
                msg="Failed to retrieve scim group ID: '%s'" % (id))
        attributes = [attribute]
    elif scim_name is not None:
        attribute = service.getByName(scim_name, idp_name)
        if attribute is None:
            module.fail_json(
                msg="Failed to retrieve scim group Name: '%s'" % (scim_name))
        attributes = [attribute]
    else:
        attributes = service.getAllByIDPName(idp_name)
    module.exit_json(changed=False, data=attributes)


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    argument_spec.update(
        name=dict(type="str", required=False),
        id=dict(type="str", required=False),
        idp_name=dict(type="str", required=True),
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
