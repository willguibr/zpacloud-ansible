.. _zpa_posture_profile_info_module:


zpa_posture_profile_info - Get details (ID and/or Name) of a posture profile resource.
======================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves a Posture Profile details from the ZPA Cloud.




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
   
      The unique name for the posture profile.

   id (str):

         The unique identifier for the posture profile.

Notes
-----


Examples
--------

.. code-block:: yaml+jinja

   - name: Gather information About All Posture Profiles
      willguibr.zpacloud.zpa_posture_profile_info:
      register: postures

   - debug:
        msg: "{{ postures }}"

    - name: Gather Details of a Specific Posture Profiles by Name
      willguibr.zpacloud.zpa_posture_profile_info:
        name: CrowdStrike_ZPA_ZTA_80
      register: posture

   - debug:
        msg: "{{ posture.data[0].id }}"

   - name: Gather Details of a Specific Posture Profiles by ID
      willguibr.zpacloud.zpa_posture_profile_info:
        id: 216196257331285223
      register: postures

   - debug:
        msg: "{{ postures }}"



Status
------
N/A


Authors
~~~~~~~

- William Guilherme (@willguibr)