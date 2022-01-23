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
    service = LSSClientTypesService(module)
    lss_client_types = service.getAll()
    module.exit_json(changed=False, data=lss_client_types)


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
