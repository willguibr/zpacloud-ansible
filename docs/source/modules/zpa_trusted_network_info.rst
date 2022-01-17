.. zpa_trusted_network_info_module:


zpa_trusted_network_info - Get details (ID and/or Name) of a machine group resource.
====================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves Trusted Network details (ID and/or Name) from the ZPA Cloud,
so it can be associated with ZPA access policy rules.




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
   
      The unique name for the Trusted Networks certificate.

   id (str):

      The unique identifier for the Trusted Networks certificate.


Notes
-----

Examples
--------

.. code-block:: yaml+jinja

    - name: Gather Details of All Trusted Network
      willguibr.zpacloud.zpa_trusted_network_info:
      register: networks
      
   - debug:
        msg: "{{ networks }}"

    - name: Gather Details of a Specific Trusted Network by Name
      willguibr.zpacloud.zpa_trusted_network_info:
        name: Corp_Trusted_Network
      register: network_name

    - debug:
      msg: "{{ network_name.data[0].id }}"

    - name: Gather Details of a Specific Trusted Network by ID
      willguibr.zpacloud.zpa_trusted_network_info:
        id: "216196257331282583"
      register: network_id

    - debug:
      msg: "{{ network_id }}"


Status
------
N/A


Authors
~~~~~~~

- William Guilherme (@willguibr)