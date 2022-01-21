#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_saml_attribute import SamlAttributeService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_saml_attribute_info
short_description: Retrieves saml attributes from a given IDP
description:
  - This module will allow the retrieval of information about a saml attributes from a given IDP
author: William Guilherme (@willguibr)
version_added: "1.0.0"
requirements:
  - supported starting from zpa_api >= 1.0
options:
  name:
    description:
      - Name of the saml attribute.
    required: false
    type: str
  id:
    description:
      - ID of the saml attribute.
    required: false
    type: str

"""

EXAMPLES = """
- name: Get Information About All SAML Attributes
  willguibr.zpacloud.zpa_saml_attribute_info:
  
- name: Get Information About Saml Attribute by Attribute Name
  willguibr.zpacloud.zpa_saml_attribute_info:
    name: DepartmentName_User
    
- name: Get Information About Saml Attribute by Attribute ID
  willguibr.zpacloud.zpa_saml_attribute_info:
    id: 216196257331285827
"""

RETURN = """
# Returns information on a specified SAML attribute.
"""


def core(module):
    saml_attr_name = module.params.get("name", None)
    saml_attr_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = SamlAttributeService(module, customer_id)
    attributes = []
    if saml_attr_id is not None:
        attribute = service.getByID(saml_attr_id)
        if attribute is None:
            module.fail_json(
                msg="Failed to retrieve saml attribute ID: '%s'" % (id))
        attributes = [attribute]
    elif saml_attr_name is not None:
        attribute = service.getByName(saml_attr_name)
        if attribute is None:
            module.fail_json(
                msg="Failed to retrieve saml attribute Name: '%s'" % (saml_attr_name))
        attributes = [attribute]
    else:
        attributes = service.getAll()
    module.exit_json(changed=False, data=attributes)


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
