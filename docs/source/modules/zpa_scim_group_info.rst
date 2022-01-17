.. _zpa_scim_group_info_module:


zpa_scim_group_info - Get details (ID and/or Name) of SCIM Group.
=================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves details of a SCIM Group in the ZPA Cloud, so it can be used
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

            The name of scim group.

      idp_name (required, type: str):

            The name of IdP storing the scim attribute header.

      id (str):

         The unique identifier for the scim attribute header.


Notes
-----

Examples
--------

.. code-block:: yaml+jinja

    - name: Gather information about all SCIM Groups
      willguibr.zpacloud.zpa_scim_group_info:
        idp_name: "SGIO-User-Okta"
      register: all_scim_group

   - debug:
        msg: "{{ all_scim_group }}"

    - name: Gather information about a SCIM Group by Name
      willguibr.zpacloud.zpa_scim_group_info:
        name: "Engineering"
        idp_name: "IdP_Name"
      register: scim_group_name

   - debug:
        msg: "{{ scim_group_name.data[0].id }}"

    - name: Gather information about a SCIM Group by ID
      willguibr.zpacloud.zpa_scim_group_info:
        id: 293480
        idp_name: "IdP_Name"
      register: scim_group_id

   debug:
        msg: "{{ scim_group_id }}"






Status
------
N/A


Authors
~~~~~~~

- William Guilherme (@willguibr)