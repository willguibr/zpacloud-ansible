.. _zpa_application_segment_info_module:


zpa_application_segment_info - Get details (ID and/or Name) of an Application Segment.
======================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves details of an Application Segment in the ZPA Cloud.




Requirements
------------
This module requires proper API credentials to be passed statically or via environment variables:

- `zpa_client_id`
- `zpa_client_secret`
- `zpa_customer_id`
   
Refer to the following help article: https://help.zscaler.com/zpa/about-api-keys

Parameters
----------

segment_group_id (str):

      The unique identifer for the segment group this application segment belongs to.

   udp_ports (:obj:`list` of :obj:`str`):

      List of udp port range pairs, e.g. ['35000', '35000'] for port 35000.

   tcp_ports (:obj:`list` of :obj:`str`):

      List of tcp port range pairs, e.g. ['22', '22'] for port 22-22, ['80', '100'] for 80-100.

   domain_names (:obj:`list` of :obj:`str`):
   
      List of domain names or IP addresses for the application segment.

   name (str):
   
      The name of the application segment.

   server_group_ids (:obj:`list` of :obj:`str`):
   
      The list of server group IDs that belong to this application segment.

   bypass_type (str):
      
      The type of bypass for the Application Segment. Accepted values are `ALWAYS`, `NEVER` and `ON_NET`.

   clientless_app_ids (:obj:`list`):
      
      List of unique IDs for clientless apps to associate with this Application Segment.
   
   config_space (str):
      
      The config space for this Application Segment. Accepted values are `DEFAULT` and `SIEM`.

   default_idle_timeout (int):
      
      The Default Idle Timeout for the Application Segment.

   default_max_age (int):
      
      The Default Max Age for the Application Segment.

   description (str):
      
      Additional information about this Application Segment.

   double_encrypt (bool):
      
      Double Encrypt the Application Segment micro-tunnel.

   enabled (bool):
      
      Enable the Application Segment.

   health_check_type (str):
      
      Set the Health Check Type. Accepted values are `DEFAULT` and `NONE`.

   health_reporting (str):
      
      Set the Health Reporting. Accepted values are `NONE`, `ON_ACCESS` and `CONTINUOUS`.

   ip_anchored (bool):
      
      Enable IP Anchoring for this Application Segment.

   is_cname_enabled (bool):
      
      Enable CNAMEs for this Application Segment.
      
   passive_health_enabled (bool):
      
      Enable Passive Health Checks for this Application Segment.

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