.. _zpa_scim_attribute_header_info_module:


zpa_scim_attribute_header_info - Get details (ID and/or Name) of SCIM Attribute Header.
=======================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves details of a SCIM Attribute Header in the ZPA Cloud, so it can be used
in access policy, timeout policy, or forwarding policy.




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

            The name of scim attribute header.

      idp_name (required, type: str):

            The name of IdP storing the scim attribute header.

      id (str):

         The unique identifier for the scim attribute header.


Notes
-----

Examples
--------

.. code-block:: yaml+jinja

    - name: Gather Information about All SCIM Attribute Header
      willguibr.zpacloud.zpa_scim_attribute_header_info:
        idp_name: IdP_Name
      register: scim

   - debug:
        msg: "{{ scim }}"

    - name: Gather Information about All SCIM Attribute Header By Name
      willguibr.zpacloud.zpa_scim_attribute_header_info:
        name: costCenter
        idp_name: IdP_Name
      register: scim_attr_name

   - debug:
        msg: "{{ scim_attr_name.data[0].id }}"

    - name: Gather Information about All SCIM Attribute Header By ID
      willguibr.zpacloud.zpa_scim_attribute_header_info:
        id: 216196257331285842
        idp_name: IdP_Name
      register: scim_attr_id

   - debug:
        msg: "{{ scim_attr_id }}"





Status
------
N/A


Authors
~~~~~~~

- William Guilherme (@willguibr)