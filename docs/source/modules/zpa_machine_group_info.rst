.. _zpa_machine_group_info_module:


zpa_machine_group_info - Get details (ID and/or Name) of a machine group resource.
==================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves a Machine Group details from the ZPA Cloud.




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
   
      The unique name for the machine group.

   id (str):

         The unique identifier for the machine group.

Notes
-----


Examples
--------

.. code-block:: yaml+jinja

    - name: Gather Details of All Machine Groups
      willguibr.zpacloud.zpa_machine_group_info:
      register: machine_groups

    - debug:
      msg: "{{ machine_groups }}"

    - name: Gather Details of a Specific Machine Group by Name
      willguibr.zpacloud.zpa_machine_group_info:
        name: "Corp_Machine_Group"
      register: machine_group_name

    - debug:
      msg: "{{ machine_group_name.data[0].id }}"

    - name: Gather Details of a Specific Machine Group by ID
      willguibr.zpacloud.zpa_machine_group_info:
        id: "216196257331282583"
      register: machine_group_id

    - debug:
      msg: "{{ machine_group_id }}"


Status
------
N/A


Authors
~~~~~~~

- William Guilherme (@willguibr)