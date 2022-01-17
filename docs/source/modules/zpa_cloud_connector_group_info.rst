.. _zpa_cloud_connector_group_info_module:


zpa_cloud_connector_group_info - Get details (ID and/or Name) of a cloud connector group resource.
===================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves a Cloud Connector Group detail from the ZPA Cloud.




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
   
      The unique name for the Cloud Connector Group.

   id (str):

      The unique identifier for the Cloud Connector Group.

Notes
-----

Examples
--------

.. code-block:: yaml+jinja

    - name: Gather Information Details of All Cloud Connector Groups
      willguibr.zpacloud.zpa_cloud_connector_group_info:
      register: all_cloud_connector_groups

    - debug:
        msg: "{{ all_cloud_connector_groups }}"

    - name: Gather Information Details of a Cloud Connector Group by Name
      willguibr.zpacloud.zpa_cloud_connector_group_info:
        name: zs-cc-vpc-096108eb5d9e68d71-ca-central-1a
      register: cloud_connector_group_name

    - debug:
        msg: "{{ cloud_connector_group_name }}"

    - name: Gather Information Details of a Cloud Connector Group by ID
      willguibr.zpacloud.zpa_cloud_connector_group_info:
        id: "216196257331292017"
      register: cloud_connector_group_id

    - debug:
        msg: "{{ cloud_connector_group_id }}"


Status
------
N/A


Authors
~~~~~~~

- William Guilherme (@willguibr)