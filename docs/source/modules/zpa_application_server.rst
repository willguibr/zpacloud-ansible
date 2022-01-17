.. _zpa_application_server_module:


zpa_application_server - Create/Update/Delete an Application Server.
====================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module creates an Application Server in the ZPA Cloud.




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

            The name of the server.

      address (str):

            The IP address of the server.

      enabled (bool):

            Enable the server.

      description (str):

            A description for the server.

      app_server_group_ids (list):

            Unique identifiers for the server groups the server belongs to.

      config_space (str):
      
            The configuration space for the server.


Notes
-----

Examples
--------

.. code-block:: yaml+jinja

    - name: Create Second Application Server
      willguibr.zpacloud_ansible.zpa_application_server:
        name: Example1
        description: Example1
        address: example.acme.com
        enabled: true
        app_server_group_ids:
          - id: "{{ server_group_id.data[0].id }}"

    - name: Create Second Application Server
      willguibr.zpacloud_ansible.zpa_application_server:
        name: Example1
        description: Example1
        address: example.acme.com
        enabled: true

Status
------
N/A


Authors
~~~~~~~

- William Guilherme (@willguibr)