========
Examples
========

What is Zscaler Private Access
==============================

The Zscaler Private Access (ZPA) service enables organizations to provide access to internal applications and services while ensuring the security of their networks.
ZPA is an easier to deploy, more cost-effective, and more secure alternative to VPNs. Unlike VPNs, which require users to connect to your network to access your enterprise applications,
ZPA allows you to give users policy-based secure access only to the internal apps they need to get their work done. With ZPA, application access does not require network access.

App Connector Group
-------------------

.. code-block:: yaml

    - name: Create First App Connector Group
      willguibr.zpacloud.zpa_app_connector_groups:
        name: "Example1"
        description: "Example1"
        enabled: true
        city_country: "California, US"
        country_code: "US"
        latitude: "37.3382082"
        longitude: "-121.8863286"
        location: "San Jose, CA, USA"
        upgrade_day: "SUNDAY"
        upgrade_time_in_secs: "66600"
        override_version_profile: true
        version_profile_id: "0"
        dns_query_type: "IPV4"

Service Edge Group
------------------

.. code-block:: yaml

   - name: Create/Update/Delete Service Edge Group
      willguibr.zpacloud.zpa_service_edge_groups:
        name: "Example"
        description: "Example1"
        enabled: true
        city_country: "California, US"
        country_code: "US"
        latitude: "37.3382082"
        longitude: "-121.8863286"
        location: "San Jose, CA, USA"
        upgrade_day: "SUNDAY"
        upgrade_time_in_secs: "66600"
        override_version_profile: true
        version_profile_id: "0"

Provisioning Key
----------------

.. code-block:: yaml

    - name: Create/Update/Delete App Connector Group Provisioning Key
      willguibr.zpacloud.zpa_provisioning_key:
        name: "App Connector Group Provisioning Key"
        association_type: "CONNECTOR_GRP"
        max_usage: "10"
        enrollment_cert_id: 6573
        zcomponent_id: 216196257331291903

    - name: Create/Update/Delete Service Edge Connector Group Provisioning Key
      willguibr.zpacloud.zpa_provisioning_key:
        name: "Service Edge Connector Group Provisioning Key"
        association_type: "CONNECTOR_GRP"
        max_usage: "10"
        enrollment_cert_id: 6573
        zcomponent_id: 216196257331291903


Application Segment
-------------------

.. code-block:: yaml

    - name: Create First Application Segment
      willguibr.zpacloud.zpa_application_segment:
        name: Example Application
        description: Example Application Test
        enabled: true
        health_reporting: ON_ACCESS
        bypass_type: NEVER
        is_cname_enabled: true
        tcp_port_range:
          - from: "8080"
            to: "8085"
        domain_names:
          - server1.example.com
          - server2.example.com
        segment_group_id: "216196257331291896"
        server_groups:
          - id: "216196257331291969"

Browser Access Application Segment
----------------------------------

.. code-block:: yaml

    - name: Create/Update/Delete a Browser Access Application Segment
      willguibr.zpacloud.zpa_browser_access:
        name: Example
        description: Example
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
        segment_group_id: "216196257331291896"
        server_groups:
          - "216196257331291969"
          
Server Group
------------

.. code-block:: yaml

    - name: Create/Update/Delete a Server Group
      willguibr.zpacloud_ansible.zpa_server_group:
        name: "Example"
        description: "Example"
        enabled: false
        dynamic_discovery: false
        app_connector_groups:
          - id: "216196257331291924"
        servers:
          - id: "216196257331291921"
        applications:
          - id: "216196257331291981"

Segment Group
-------------

.. code-block:: yaml

    - name: Create/Update/Delete a Server Group
      willguibr.zpacloud.zpa_segment_group:
        config_space: "DEFAULT"
        name: Example Segment Group
        description: Example Segment Group
        enabled: true
        policy_migrated: true
        tcp_keep_alive_enabled: "1"
