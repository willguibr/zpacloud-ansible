#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: zpa_application_server
short_description: Create an application server in the ZPA Cloud.
description:
    - This module creates/update/delete an application server in the ZPA Cloud.
author:
    - William Guilherme (@willguibr)
version_added: '1.0.0'
options:
    client_id:
        description: ""
        required: false
        type: str
    client_secret:
        description: ""
        required: false
        type: str
    customer_id:
        description: ""
        required: false
        type: str
    name:
        description:
            - This field defines the name of the server to create.
        required: True
        type: str
    id:
        description: ""
        required: false
        type: str
    address:
        description: ""
        required: true
        type: str
    app_server_group_ids:
        description:
            - This field defines the list of server groups IDs.
        required: False
        type: list
        elements: str
    enabled:
        description:
            - This field defines the status of the server, true or false.
        required: False
        type: bool
    description:
        description:
            - This field defines the description of the server to create.
        required: False
        type: str
    config_space:
        description:
            - This field defines the type of the server, DEFAULT or SIEM.
        required: False
        type: str
        default: "DEFAULT"
        choices: ["DEFAULT", "SIEM"]
    state:
        description: "Whether the app should be present or absent."
        type: str
        choices:
            - present
            - absent
        default: present
"""

EXAMPLES = r"""
- name: Create Second Application Server
  willguibr.zpacloud.zpa_application_server:
    name: Example1
    description: Example1
    address: example.acme.com
    enabled: true
    app_server_group_ids: []
"""

RETURN = r"""
# The newly created application server resource record.
"""


from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_application_server import ApplicationServerService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper


def core(module):
    state = module.params.get("state", None)
    customer_id = module.params.get("customer_id", None)
    service = ApplicationServerService(module, customer_id)
    application_server = dict()
    params = [
        "id",
        "name",
        "description",
        "address",
        "enabled",
        "app_server_group_ids",
        "config_space",
    ]
    for param_name in params:
        application_server[param_name] = module.params.get(param_name, None)
    existing_application_server = service.getByIDOrName(
        application_server.get("id"), application_server.get("name"))
    if existing_application_server is not None:
        id = existing_application_server.get("id")
        existing_application_server.update(application_server)
        existing_application_server["id"] = id
    if state == "present":
        if existing_application_server is not None:
            """Update"""
            service.update(existing_application_server)
            module.exit_json(changed=True, data=existing_application_server)
        else:
            """Create"""
            application_server = service.create(application_server)
            module.exit_json(changed=False, data=application_server)
    elif state == "absent":
        if existing_application_server is not None:
            service.delete(existing_application_server.get("id"))
            module.exit_json(changed=False, data=existing_application_server)
    module.exit_json(changed=False, data={})


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    id_name_spec = dict(type='list', elements='dict', options=dict(id=dict(
        type='str', required=False), name=dict(type='str', required=False)), required=False)
    argument_spec.update(
        id=dict(type="str"),
        name=dict(type='str', required=True),
        description=dict(type='str', required=False),
        address=dict(type='str', required=True),
        enabled=dict(type='bool', required=False),
        app_server_group_ids=dict(type='list', elements='str', required=False),
        config_space=dict(type='str', required=False,
                          default="DEFAULT", choices=["DEFAULT", "SIEM"]),
        state=dict(type="str", choices=[
                   "present", "absent"], default="present"),
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
