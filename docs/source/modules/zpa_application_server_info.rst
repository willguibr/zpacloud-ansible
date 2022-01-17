.. _zpa_application_server_info_module:


zpa_application_server_info - Get details (ID and/or Name) of an Application Server.
====================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves details of an Application Server in the ZPA Cloud.




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

            The name of the server.


Notes
-----

Examples
--------

.. code-block:: yaml+jinja

      - name: Gather Details of All Application Segments
      willguibr.zpacloud.zpa_application_segment_info:
      register: all_app_segments

      - debug:
      msg: "{{ all_app_segments }}"

      - name: Gather Details of a Specific Application Segments by Name
      willguibr.zpacloud.zpa_application_segment_info:
         name: "Example Application Segment"
      register: app_segment_name

      - debug:
      msg: "{{ app_segment_name }}"

      - name: Gather Details of a Specific Application Segments by ID
      willguibr.zpacloud.zpa_application_segment_info:
         id: "216196257331291981"
      register: app_segment_id

      - debug:
      msg: "{{ app_segment_id }}"


Status
------
N/A


Authors
~~~~~~~

- William Guilherme (@willguibr)