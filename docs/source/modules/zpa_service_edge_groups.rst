.. _zpa_service_edge_groups_module:


zpa_service_edge_groups - Create/Update/Delete an Service Edge Group.
=====================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------
   
This module is used to create an Service Edge Group in the ZPA Cloud.




Requirements
------------
This module requires proper API credentials to be passed statically or via environment variables:

- `zpa_client_id`
- `zpa_client_secret`
- `zpa_customer_id`

Refer to the following help article: https://help.zscaler.com/zpa/about-api-keys

Parameters
----------


      latitude (Required, type: str): The latitude representing the physical location of the ZPA Service Edges in this group.

      longitude (Required, type: str): The longitude representing the physical location of the ZPA Service Edges in this group.

      location (Required, type: str): The name of the physical location of the ZPA Service Edges in this group.

      name (Required, type: str): The name of the Service Edge Group.

      cityCountry (str):
         The City and Country for where the App Connectors are located. Format is:
                ``<City>, <Country Code>`` e.g. ``Sydney, AU``
      
      country_code (str):
         The ISO<std> Country Code that represents the country where the App Connectors are located.
      
      enabled (bool):
         Is the Service Edge Group enabled? Defaults to ``True``.
      
      is_public (bool):
         Is the Service Edge publicly accessible? Defaults to ``False``.
            
      override_version_profile (bool):
         Override the local App Connector version according to ``version_profile``. Defaults to ``False``.
      
      service_edge_ids (list):
         A list of unique ids of ZPA Service Edges that belong to this Service Edge Group.
      
      trusted_network_ids (list):
         A list of unique ids of Trusted Networks that are associated with this Service Edge Group.
      
      upgrade_day (str):
         The day of the week that upgrades will be pushed to the App Connector.
      
      upgrade_time_in_secs (str):
         The time of the day that upgrades will be pushed to the App Connector.
      
      version_profile (str):
         The version profile to use. This will automatically set ``override_version_profile`` to True.
            Accepted values are: ``default``, ``previous_default`` and ``new_release``

Notes
-----

Examples
--------

.. code-block:: yaml+jinja

    - name: Create/update/delete an service edge groups
      willguibr.zpacloud.zpa_service_edge_groups:
        name: "Example"
        description: "Example"
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

Status
------
N/A


Authors
~~~~~~~

- William Guilherme (@willguibr)