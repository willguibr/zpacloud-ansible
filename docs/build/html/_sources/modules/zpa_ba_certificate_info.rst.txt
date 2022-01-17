.. _zpa_ba_certificate_info_module:


zpa_ba_certificate_info - Get details (ID and/or Name) of a browser certificate resource.
=========================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves Browser Certificate details (ID and/or Name) from the ZPA Cloud,
so it can be associated with a browser access application segment resource.




Requirements
------------
This module requires proper API credentials to be passed statically or via environment variables:

- `zpa_client_id`
- `zpa_client_secret`
- `zpa_customer_id`

Refer to the following help article: https://help.zscaler.com/zpa/about-api-keys

Parameters
----------

   name (str):
   
      The unique name for the Browser Access certificate.

   certificate_id (str):

      The unique identifier for the Browser Access certificate.


Notes
-----

Examples
--------

.. code-block:: yaml+jinja

    - name: Gather Details of All Browser Certificates
      willguibr.zpacloud.zpa_ba_certificate_info:
      register: certificates

    - debug:
      msg: "{{ certificates }}"

    - name: Gather Details of a Specific Browser Certificates by Name
      willguibr.zpacloud.zpa_ba_certificate_info:
        name: crm.acme.com
      register: certificate_name

    - debug:
      msg: "{{ certificate_name }}"

    - name: Gather Details of a Specific Browser Certificates by ID
      willguibr.zpacloud.zpa_ba_certificate_info:
        id: "216196257331282583"
      register: certificate_id

    - debug:
      msg: "{{ certificate_id }}"


Status
------
N/A


Authors
~~~~~~~

- William Guilherme (@willguibr)