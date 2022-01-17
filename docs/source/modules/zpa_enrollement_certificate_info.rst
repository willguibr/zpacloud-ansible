.. _zpa_enrollement_certificate_info_module:


zpa_enrollement_certificate_info - Get details (ID and/or Name) of an enrollment certificate resource.
======================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves a Enrollment Certificate detail from the ZPA Cloud.




Requirements
------------
This module requires proper API credentials to be passed statically or via environment variables:

- `zpa_client_id`
- `zpa_client_secret`
- `zpa_customer_id`

Refer to the following help article: https://help.zscaler.com/zpa/about-api-keys

Parameters
----------

   name (required, type: str):
   
      The unique name for the Customer Version Profile.

   id (str):

      The unique identifier for the Customer Version Profile.

Notes
-----


Examples
--------

.. code-block:: yaml+jinja

    - name: Gather Information Details of All Enrollment Certificates
      willguibr.zpacloud.zpa_enrollment_cert_info:
      register: all_enrollment_certs

    - debug:
        msg: "{{ all_enrollment_certs }}"

    - name: Gather Information Details of the Root Enrollment Certificates by Name
      willguibr.zpacloud.zpa_enrollment_cert_info:
        name: "Root"
      register: enrollment_cert_root

    - debug:
        msg: "{{ enrollment_cert_root }}"

    - name: Gather Information Details of the Client Enrollment Certificates by Name
      willguibr.zpacloud.zpa_enrollment_cert_info:
        name: "Client"
      register: enrollment_cert_client

    - debug:
        msg: "{{ enrollment_cert_client }}"

    - name: Gather Information Details of the Connector Enrollment Certificates by Name
      willguibr.zpacloud.zpa_enrollment_cert_info:
        name: "Connector"
      register: enrollment_cert_connector

    - debug:
        msg: "{{ enrollment_cert_connector }}"

    - name: Gather Information Details of the Service Edge Enrollment Certificates by Name
      willguibr.zpacloud.zpa_enrollment_cert_info:
        name: "Service Edge"
      register: enrollment_cert_service_edge

    - debug:
        msg: "{{ enrollment_cert_service_edge }}"

    - name: Gather Information Details of the Isolation Client Enrollment Certificates by Name
      willguibr.zpacloud.zpa_enrollment_cert_info:
        name: "Isolation Client"
      register: enrollment_cert_isolation_client

    - debug:
        msg: "{{ enrollment_cert_isolation_client }}"


Status
------
N/A


Authors
~~~~~~~

- William Guilherme (@willguibr)