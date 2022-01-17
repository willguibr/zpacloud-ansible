.. _zpa_segment_group_module:


zpa_segment_group - Create/Update/Delete an Segment Group.
==========================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module creates a Segment Group in the ZPA Cloud.




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
   
         The name of the new segment group.

   enabled (type: bool):

         Enable the segment group. Defaults to False.

   application_ids (:obj:`list` of :obj:`dict`):

         Unique application IDs to associate with the segment group.

   config_space (type: str):
         The config space for the segment group. Can either be DEFAULT or SIEM.

   description (type: str):

         A description for the segment group.

   policy_migrated (type: bool):


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