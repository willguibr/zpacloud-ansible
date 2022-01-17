.. _zpa_segment_group_info_module:


zpa_segment_group_info - Get details (ID and/or Name) of a segment group resource.
==================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves Segment Group details from the ZPA Cloud.




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
   
      The unique name for the segment group.

   id (str):

         The unique identifier for the segment group.

Notes
-----


Examples
--------

.. code-block:: yaml+jinja

    - name: Gather Detail Information of All Segment Groups
      willguibr.zpacloud.zpa_segment_group_info:
      register: all_segment_group

    - debug:
        msg: "{{ all_segment_group }}"

    - name: Gather Details of All Segment Groups by Name
      willguibr.zpacloud.zpa_segment_group_info:
        name: Example1
      register: segment_group_name

    - debug:
        msg: "{{ segment_group_name.data[0].id }}"

    - name: Gather Details of All Segment Groups by ID
      willguibr.zpacloud.zpa_segment_group_info:
        id: "216196257331291969"
      register: segment_group_id

    - debug:
        msg: "{{ segment_group_id }}"


Status
------
N/A


Authors
~~~~~~~

- William Guilherme (@willguibr)