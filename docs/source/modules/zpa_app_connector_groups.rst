.. _zpa_app_connector_groups_module:


zpa_app_connector_groups - Create/Update/Delete an App Connector Group.
=======================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------
   
This module is used to create an App Connector Group in the ZPA Cloud.




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

      - name: Create First App Connector Group Example1
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


Status
------
N/A


Authors
~~~~~~~

- William Guilherme (@willguibr)