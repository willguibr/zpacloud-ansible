.. _zpa_browser_access_info_module:


zpa_browser_access_info - Get details (ID and/or Name) of a browser access application segment.
===============================================================================================

.. contents::
   :local:
   :depth: 1

Synopsis
--------

This module retrieves Browser Access Application Segment details (ID and/or Name) from the ZPA Cloud.



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
   
      The unique name for the browser access application segment.

   certificate_id (str):

      The unique identifier for the browser access application segment.


Notes
-----

Examples
--------

.. code-block:: yaml+jinja

    - name: Gather Details of All Browser Access App Segment
      willguibr.zpacloud.zpa_browser_access_info:
      register: ba_app_segment

    - debug:
      msg: "{{ ba_app_segment }}"

    - name: Gather Details of a Browser Access App Segment by Name
      willguibr.zpacloud.zpa_browser_access_info:
        name: crm.acme.com
      register: ba_app_segment_name

    - debug:
      msg: "{{ ba_app_segment_name }}"

    - name: Gather Details of a Browser Access App Segment by ID
      willguibr.zpacloud.zpa_browser_access_info:
        id: "216196257331282583"
      register: ba_app_segment_id

    - debug:
      msg: "{{ ba_app_segment_id }}"


Status
------
N/A


Authors
~~~~~~~

- William Guilherme (@willguibr)