.. _zpa_idp_controller_info_module:


zpa_idp_controller_info - Get details (ID and/or Name) of an idp controller resource.
=====================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves an IdP Controller detail from the ZPA Cloud.




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
   
      The unique name for the IdP.

   idp_id (str):

         The unique identifier for the IdP.

Notes
-----


Examples
--------

.. code-block:: yaml+jinja

    - name: Gather Details of All IdP Controllers
      willguibr.zpacloud.zpa_idp_controller_info:
      register: idp_controllers

    - debug:
      msg: "{{ idp_controllers }}"

    - name: Gather Details of a Specific IdP Controller by Name
      willguibr.zpacloud.zpa_idp_controller_info:
        name: User_IdP_Name
      register: idp_name

    - debug:
      msg: "{{ idp_name.data[0].id }}"

    - name: Gather Details of a Specific IdP Controller by ID
      willguibr.zpacloud.zpa_idp_controller_info:
        id: "216196257331282583"
      register: idp_id

    - debug:
      msg: "{{ idp_id }}"


Status
------
N/A


Authors
~~~~~~~

- William Guilherme (@willguibr)