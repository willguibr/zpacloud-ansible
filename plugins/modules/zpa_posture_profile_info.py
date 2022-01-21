#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_posture_profile import PostureProfileService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_posture_profile_info
short_description: Retrieves details of a posture profile resource.
description:
  - This module will allow the retrieval of information about a posture profile resource.
author: William Guilherme (@willguibr)
version_added: "1.0.0"
requirements:
  - supported starting from zpa_api >= 1.0
options:
  name:
    description:
      - Name of the posture profile.
    required: false
    type: str
  id:
    description:
      - ID of the posture profile.
    required: false
    type: str
"""

EXAMPLES = """
- name: Get Information About All Posture Profiles
  willguibr.zpacloud.zpa_posture_profile_info:

- name: Get Details of a Specific Posture Profile by ID
  willguibr.zpacloud.zpa_posture_profile_info:
    id: "216196257331282583"
     
- name: Get Details of a Specific Posture Profile by Name
  willguibr.zpacloud.zpa_posture_profile_info:
    name: CrowdStrike_ZPA_Pre-ZTA
"""

RETURN = """
# Returns information on a specified posture profile.
"""


def core(module):
    posture_name = module.params.get("name", None)
    posture_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = PostureProfileService(module, customer_id)
    postures = []
    if posture_id is not None:
        posture = service.getByID(posture_id)
        if posture is None:
            module.fail_json(
                msg="Failed to retrieve Posture Profile ID: '%s'" % (id))
        postures = [posture]
    elif posture_name is not None:
        posture = service.getByName(posture_name)
        if posture is None:
            module.fail_json(
                msg="Failed to retrieve Posture Profile Name: '%s'" % (posture_name))
        postures = [posture]
    else:
        postures = service.getAll()
    module.exit_json(changed=False, data=postures)


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
