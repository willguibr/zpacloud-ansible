.. _zpa_application_segment_module
----------------------------------

zpa_application_segment -- Create/Update/Delete an Application Segment.
========================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Create/Update/Delete an Application Segment.


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

    - name: Create an Application Segment
      willguibr.zpacloud_ansible.zpa_application_segment:
        state: absent
        name: Example Application
        description: Example Application Test
        enabled: true
        health_reporting: ON_ACCESS
        bypass_type: NEVER
        is_cname_enabled: true
        tcp_port_range:
          - from: "80"
            to: "80"
        domain_names:
          - crm1.example.com
          - crm2.example.com
        segment_group_id: "{{ segment_group_id.data.0.id }}"
        server_groups:
          - id: "{{ server_group_id.data.0.id }}"

Status
------





Authors
~~~~~~~

- William Guilherme (@willguibr)
