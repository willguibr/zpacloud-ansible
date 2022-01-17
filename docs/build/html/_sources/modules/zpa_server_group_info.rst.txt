.. _zpa_server_group_info_module:


zpa_server_group_info - Get details (ID and/or Name) of a server group resource.
================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves Server Group details from the ZPA Cloud.




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
   
      The unique name for the server group.

   id (str):

         The unique identifier for the server group.

Notes
-----

N/A


Examples
--------

.. code-block:: yaml+jinja

    - name: Gather Details of All Server Groups
      willguibr.zpacloud.zpa_server_group_info:
      register: all_server_groups

    - debug:
        msg: "{{ all_server_groups }}"

    - name: Gather Details of All Server Groups by Name
      willguibr.zpacloud.zpa_server_group_info:
        name: Example1
      register: server_group_name

    - debug:
        msg: "{{ server_group_name.data[0].id }}"

    - name: Gather Details of All Server Groups by ID
      willguibr.zpacloud.zpa_server_group_info:
        id: "216196257331291969"
      register: server_group_id

    - debug:
        msg: "{{ server_group_id }}"


Status
------
N/A


Authors
~~~~~~~

- William Guilherme (@willguibr)