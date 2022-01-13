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
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_application_server import ApplicationServerService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_application_server_info
short_description: Gather information about an server group
description:
    - This module can be used to gather information about an server group.
author:
    - William Guilherme (@willguibr)
version_added: '1.0.0'
options:
  name:
    description:
     - Name of the server group.
    required: false
    type: str
  id:
    description:
     - ID of the server group.
    required: false
    type: str
"""

EXAMPLES = """
- name: Gather Information Details of All Application Servers
    willguibr.zpacloud.zpa_application_server_info:
    register: all_app_server

- debug:
    msg: "{{ all_app_server }}"

- name: Gather Information Details of an Application Server by Name
    willguibr.zpacloud.zpa_application_server_info:
    name: server1.acme.com
    register: app_server_name

- debug:
    msg: "{{ app_server_name }}"

- name: Gather Information Details of an Application Server by ID
    willguibr.zpacloud.zpa_application_server_info:
    id: "216196257331291921"
    register: app_server_id

- debug:
    msg: "{{ app_server_id }}"
"""

RETURN = """
# Default return values
"""

def core(module):
    application_server_name = module.params.get("name", None)
    application_server_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = ApplicationServerService(module, customer_id)
    application_servers = []
    if application_server_id is not None:
        application_server = service.getByID(application_server_id)
        if application_server is None:
            module.fail_json(
                msg="Failed to retrieve application server ID: '%s'" % (id))
        application_servers = [application_server]
    elif application_server_name is not None:
        application_server = service.getByName(application_server_name)
        if application_server is None:
            module.fail_json(
                msg="Failed to retrieve application server Name: '%s'" % (application_server_name))
        application_servers = [application_server]
    else:
        application_servers = service.getAll()
    module.exit_json(changed=False, data=application_servers)


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
