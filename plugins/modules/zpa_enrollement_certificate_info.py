#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_enrollement_certificate import EnrollementCertificateService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_enrollement_certificate_info
short_description: Retrieves enrollment certificate information.
description:
  - This module will allow the retrieval of information about a Enrollment Certificate detail from the ZPA Cloud.
author: William Guilherme (@willguibr)
version_added: "1.0.0"
requirements:
  - supported starting from zpa_api >= 1.0
options:
  name:
    description:
      - Name of the browser certificate.
    required: false
    type: str
  id:
    description:
      - ID of the browser certificate.
    required: false
    type: str
"""

EXAMPLES = """
- name: Gather Information Details of All Enrollment Certificates
  willguibr.zpacloud.zpa_enrollment_cert_info:

- name: Gather Information Details of the Root Enrollment Certificates by Name
  willguibr.zpacloud.zpa_enrollment_cert_info:
    name: "Root"

- name: Gather Information Details of the Client Enrollment Certificates by Name
  willguibr.zpacloud.zpa_enrollment_cert_info:
    name: "Client"

- name: Gather Information Details of the Connector Enrollment Certificates by Name
  willguibr.zpacloud.zpa_enrollment_cert_info:
    name: "Connector"

- name: Gather Information Details of the Service Edge Enrollment Certificates by Name
  willguibr.zpacloud.zpa_enrollment_cert_info:
    name: "Service Edge"

- name: Gather Information Details of the Isolation Client Enrollment Certificates by Name
  willguibr.zpacloud.zpa_enrollment_cert_info:
    name: "Isolation Client"
    
"""

RETURN = """
# Returns information on a specified Enrollment Certificate.
"""

def core(module):
    certificate_name = module.params.get("name", None)
    certificate_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = EnrollementCertificateService(module, customer_id)
    certificates = []
    if certificate_id is not None:
        certificate = service.getByID(certificate_id)
        if certificate is None:
            module.fail_json(
                msg="Failed to retrieve Enrollement Certificate ID: '%s'" % (id))
        certificates = [certificate]
    elif certificate_name is not None:
        certificate = service.getByName(certificate_name)
        if certificate is None:
            module.fail_json(
                msg="Failed to retrieve Enrollement Certificate Name: '%s'" % (certificate_name))
        certificates = [certificate]
    else:
        certificates = service.getAll()
    module.exit_json(changed=False, data=certificates)


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
