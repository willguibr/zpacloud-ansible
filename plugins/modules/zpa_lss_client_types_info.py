#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_lss_client_types import LSSClientTypesService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_lss_client_types_info
short_description: Retrieves LSS Client Types Information.
description:
  - This module will allow the retrieval of LSS (Log Streaming Services) Client Types information from the ZPA Cloud. This can then be associated with the source_log_type parameter when creating an LSS Resource.
author: William Guilherme (@willguibr)
version_added: "1.0.0"
requirements:
  - supported starting from zpa_api >= 2.0
options:
  name:
    description:
      - Name of the LSS client type.
    required: false
    type: str
"""

EXAMPLES = """
- name: Get Details About All LSS Client Types
  willguibr.zpacloud.zpa_lss_client_types_info:
  register: lss_client_typeps

- debug:
    msg: "{{ lss_client_typeps }}"

"""

RETURN = """
data:
    description: Trusted Network information
    returned: success
    elements: dict
    type: list
    sample: [
      {
      }
    ]
"""


def core(module):
    lss_client_type_name = module.params.get("name", None)
    lss_client_type_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = LSSClientTypesService(module, customer_id)
    lss_client_types = []
    if lss_client_type_id is not None:
        lss_client_type = service.getByID(lss_client_type_id)
        if lss_client_type is None:
            module.fail_json(
                msg="Failed to retrieve LSS Client Types ID: '%s'" % (id))
        lss_client_types = [lss_client_type]
    elif lss_client_type_name is not None:
        lss_client_type = service.getByName(lss_client_type_name)
        if lss_client_type is None:
            module.fail_json(
                msg="Failed to retrieve LSS Client Type Name: '%s'" % (lss_client_type_name))
        lss_client_types = [lss_client_types]
    else:
        lss_client_types = service.getAll()
    module.exit_json(changed=False, data=lss_client_types)


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    argument_spec.update(
        zpn_client_type_exporter=dict(type="str", required=False),
        zpn_client_type_machine_tunnel=dict(type="str", required=False),
        zpn_client_type_ip_anchoring=dict(type="str", required=False),
        zpn_client_type_edge_connector=dict(type="str", required=False),
        zpn_client_type_zapp=dict(type="str", required=False),
        zpn_client_type_slogger=dict(type="str", required=False),
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
