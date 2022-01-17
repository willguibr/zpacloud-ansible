.. _zpa_server_group_module:


zpa_server_group - Create/Update/Delete an Server Group.
==========================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module creates a Server Group in the ZPA Cloud.




Requirements
------------
This module requires proper API credentials to be passed statically or via environment variables:

- `zpa_client_id`
- `zpa_client_secret`
- `zpa_customer_id`

Refer to the following help article: https://help.zscaler.com/zpa/about-api-keys

Parameters
----------

   name (Required, type: `str`):
         The name for the server group.

   app_connector_group_ids (Required, type :obj:`list` of :obj:`str`):

         A list of application connector IDs that will be attached to the server group.

   Optional params.

      application_ids (Required, type :obj:`list` of :obj:`str`):

         A list of unique IDs of applications to associate with this server group.

      config_space (Optional, type: `str`):
         
         The configuration space. Accepted values are `DEFAULT` or `SIEM`.

      description (Optional, type: `str`):

         Additional information about the server group.

      enabled (Optional, type: `bool`):
      
         Enable the server group.

      ip_anchored (Optional, type: `bool`):
      
         Enable IP Anchoring.

      dynamic_discovery (Optional, type: `bool`):
      
         Enable Dynamic Discovery.

      server_ids (Optional, type :obj:`list` of :obj:`str`):

         A list of unique IDs of servers to associate with this server group.


Notes
-----

N/A


Examples
--------

.. code-block:: yaml+jinja

    - name: Create/Update/Delete a Server Group
      willguibr.zpacloud.zpa_server_group:
        name: "Example"
        description: "Example"
        enabled: false
        dynamic_discovery: true
        app_connector_groups:
          - id: "216196257331291924"

.. code-block:: yaml+jinja

    - name: Create/Update/Delete a Server Group
      willguibr.zpacloud.zpa_server_group:
        name: "Example"
        description: "Example"
        enabled: false
        dynamic_discovery: false
        app_connector_groups:
          - id: "216196257331291924"
        servers:
          - id: "216196257331291921"

Status
------
N/A


Authors
~~~~~~~

- William Guilherme (@willguibr)