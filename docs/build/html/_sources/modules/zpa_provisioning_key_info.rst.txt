.. _zpa_provisioning_key_info_module:


zpa_provisioning_key_info - Get details (ID and/or Name) of a Provisioning Key by association type
==================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves details of a Provisioning Key by association type (CONNECTOR_GRP or SERVICE_EDGE_GRP) in the ZPA Cloud.




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
   
      The unique name for the Provisioning Key.

   association_type (required, type: str):

      The association type for the Provisioning Key (CONNECTOR_GRP or SERVICE_EDGE_GRP).

Notes
-----


Examples
--------

.. code-block:: yaml+jinja

   - name: Gather Details of All CONNECTOR_GRP Provisioning Keys
   willguibr.zpacloud.zpa_provisioning_key_info:
      association_type: "CONNECTOR_GRP"
   register: all_connector_grp_keys

   - debug:
      msg: "{{ all_connector_grp_keys }}"

   - name: Gather Details of All CONNECTOR_GRP Provisioning Keys by Name
   willguibr.zpacloud.zpa_provisioning_key_info:
      name: "Example App Connector Group"
      association_type: "CONNECTOR_GRP"
   register: connector_grp_key_name

   - debug:
      msg: "{{ connector_grp_key_name.data[0].id }}"

   - name: Gather Details of All CONNECTOR_GRP Provisioning Keys by ID
   willguibr.zpacloud.zpa_provisioning_key_info:
      id: "8691"
      association_type: "CONNECTOR_GRP"
   register: connector_grp_key_id

   - debug:
      msg: "{{ connector_grp_key_id }}"

.. code-block:: yaml+jinja

    - name: Gather Details of All SERVICE_EDGE_GRP Provisioning Keys
      willguibr.zpacloud.zpa_provisioning_key_info:
        association_type: "SERVICE_EDGE_GRP"
      register: all_edge_grp_key_name

    - debug:
        msg: "{{ all_edge_grp_key_name }}"

    - name: Gather Details of All SERVICE_EDGE_GRP Provisioning Keys by Name
      willguibr.zpacloud.zpa_provisioning_key_info:
        name: "Example Service Edge Group"
        association_type: "SERVICE_EDGE_GRP"
      register: edge_grp_key_name

    - debug:
        msg: "{{ edge_grp_key_name.data[0].id }}"

    - name: Gather Details of All SERVICE_EDGE_GRP Provisioning Keys by ID
      willguibr.zpacloud.zpa_provisioning_key_info:
        id: "8691"
        association_type: "SERVICE_EDGE_GRP"
      register: edge_grp_key_id

    - debug:
        msg: "{{ edge_grp_key_id }}"

Status
------
N/A


Authors
~~~~~~~

- William Guilherme (@willguibr)