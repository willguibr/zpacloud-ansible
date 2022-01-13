#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Ansible module to manage Zscaler Private Access (ZPA) 2022
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_lss_client_types import LSSClientTypesService
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = r"""
---
author: William Guilherme (@willguibr)
description:
  - Provides details about a specific trusted network created in the Zscaler Private Access Mobile Portal
module: zpa_trusted_network_info
short_description: Provides details about a specific trusted network created in the Zscaler Private Access Mobile Portal
version_added: "1.0.0"
requirements:
  - supported starting from zpa_api >= 1.0
options:
  name:
    description:
      - Name of the trusted network.
    required: false
    type: str
  id:
    description:
      - ID of the trusted network.
    required: false
    type: str

"""

EXAMPLES = """
- name: trusted network
  hosts: localhost
  tasks:
    - name: Gather information about all trusted network
      willguibr.zpacloud_ansible.zpa_trusted_network_info:
        #name: Corp-Trusted-Networks
        id: 216196257331282234
      register: networks
    - name: networks
      debug:
        msg: "{{ networks }}"

"""

RETURN = r"""
data:
    description: Trusted Network information
    returned: success
    elements: dict
    type: list
    sample: [
      {
          "id": "216196257331282234",
          "modified_time": "1631935891",
          "creation_time": "1625992655",
          "modified_by": "72057594037928115",
          "name": "Corp-Trusted-Networks",
          "network_id": "869fbea4-799d-422a-984f-d40fbe53bc02",
          "zscaler_cloud": "zscalerthree"
      }
    ]
"""


def core(module):
    machine_group_name = module.params.get("name", None)
    machine_group_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = LSSClientTypesService(module, customer_id)
    machine_groups = []
    if machine_group_id is not None:
        machine_group = service.getByID(machine_group_id)
        if machine_group is None:
            module.fail_json(
                msg="Failed to retrieve Machine Group ID: '%s'" % (id))
        machine_groups = [machine_group]
    elif machine_group_name is not None:
        machine_group = service.getByName(machine_group_name)
        if machine_group is None:
            module.fail_json(
                msg="Failed to retrieve Machine Group Name: '%s'" % (machine_group_name))
        machine_groups = [machine_groups]
    else:
        machine_groups = service.getAll()
    module.exit_json(changed=False, data=machine_groups)


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
