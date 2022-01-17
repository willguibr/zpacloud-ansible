.. _zpa_service_edge_groups_info_module:


zpa_service_edge_groups_info - Get details (ID and/or Name) of a Service Edge Group.
======================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves details of a Service Edge Group in the ZPA Cloud.




Requirements
------------
This module requires proper API credentials to be passed statically or via environment variables:

- `zpa_client_id`
- `zpa_client_secret`
- `zpa_customer_id`

Refer to the following help article: https://help.zscaler.com/zpa/about-api-keys

Parameters
----------

Notes
-----

Examples
--------

.. code-block:: yaml+jinja

    - name: Gather information about all Service Edge Groups
      willguibr.zpacloud.zpa_service_edge_groups_info:
      register: service_edge

   - debug:
        msg: "{{ service_edge }}"

    - name: Gather information about a Service Edge Group by Name
      willguibr.zpacloud.zpa_service_edge_groups_info:
        name: "Canada Service Edge Group"
      register: service_edge_name

   - debug:
        msg: "{{ service_edge_name.data[0].id }}"

   - name: Gather information about all Service Edge Groups
      willguibr.zpacloud.zpa_service_edge_groups_info:
        id: "216196257331292046"
      register: service_edge

   - debug:
        msg: "{{ service_edge }}"


Status
------
N/A


Authors
~~~~~~~

- William Guilherme (@willguibr)