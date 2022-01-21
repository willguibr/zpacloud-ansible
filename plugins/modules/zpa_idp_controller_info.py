#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_idp_controller import IDPControllerService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_idp_controller_info
short_description: Retrieves Identity Provider information.
description:
  - This module will allow the retrieval of information about an Identity Provider (IdP) detail from the ZPA Cloud.
author:
  - William Guilherme (@willguibr)
version_added: "1.0.0"
options:
  name:
    description:
      - Name of the Identity Provider.
    required: true
    type: str
  id:
    description:
      - ID of the Identity Provider.
    required: false
    type: str
"""

EXAMPLES = """
- name: Get Details of All IdP Controllers
  willguibr.zpacloud.zpa_idp_controller_info:

- name: Get Details of a Specific IdP Controller by Name
  willguibr.zpacloud.zpa_idp_controller_info:
    name: User_IdP_Name

- name: Get Details of a Specific IdP Controller by ID
  willguibr.zpacloud.zpa_idp_controller_info:
    id: "216196257331282583"  
"""

RETURN = """
# Returns information on a specified Identity Provider.
"""

def core(module):
    idp_name = module.params.get("name", None)
    idp_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = IDPControllerService(module, customer_id)
    idp_controllers = []
    if idp_id is not None:
        idp_controller = service.getByID(idp_id)
        if idp_controller is None:
            module.fail_json(
                msg="Failed to retrieve IDP Controller ID: '%s'" % (id))
        idp_controllers = [idp_controller]
    elif idp_name is not None:
        idp_controller = service.getByName(idp_name)
        if idp_controller is None:
            module.fail_json(
                msg="Failed to retrieve IDP Controller Name: '%s'" % (idp_name))
        idp_controllers = [idp_controller]
    else:
        idp_controller = service.getAll()
    module.exit_json(changed=False, data=idp_controllers)


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
