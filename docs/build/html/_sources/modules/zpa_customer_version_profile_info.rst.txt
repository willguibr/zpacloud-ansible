.. _zpa_customer_version_profile_info_module:


zpa_customer_version_profile_info - Get details (ID and/or Name) of a customer version profile.
===============================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves a Customer Version Profile detail from the ZPA Cloud.




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
   
      The unique name for the Customer Version Profile.

   id (str):

      The unique identifier for the Customer Version Profile.

Notes
-----

Customer Version Profiles are of 3 name types:

- name: Default, and id: "0"
- name: Previous Default and id: "1"
- name: New Release and id: "2"

Examples
--------

.. code-block:: yaml+jinja

    - name: Gather Information Details of All Customer Version Profiles
      willguibr.zpacloud.zpa_customer_version_profile_info:
      register: all_customer_version_profiles

    - debug:
        msg: "{{ all_customer_version_profiles }}"

    - name: Gather Information Details of a Cloud Connector Group by Name
      willguibr.zpacloud.zpa_customer_version_profile_info:
        name: "New Release"
      register: version_profile_name

    - debug:
        msg: "{{ version_profile_name }}"

    - name: Gather Information Details of a Cloud Connector Group by ID
      willguibr.zpacloud.zpa_customer_version_profile_info:
        id: "2"
      register: version_profile_id

    - debug:
        msg: "{{ version_profile_id }}"


Status
------
N/A


Authors
~~~~~~~

- William Guilherme (@willguibr)