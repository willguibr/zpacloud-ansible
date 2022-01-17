.. _zpa_provisioning_key_module:


zpa_provisioning_key - Create/Update/Delete a Provisioning Key by association type
==================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module to create a Provisioning Key by association type (CONNECTOR_GRP or SERVICE_EDGE_GRP) in the ZPA Cloud 




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
   
      The unique name for the Provisioning Key.

   association_type (required, type: str):

      The association type for the Provisioning Key (CONNECTOR_GRP or SERVICE_EDGE_GRP).

   enrollment_cert_id (required, type: str):

      Unique ID of the enrollment certificate that can be used for this provisioning key.

   zcomponent_id (required, type: str):

      Unique ID of the existing App Connector or Service Edge Group.


Notes
-----

N/A


Examples
--------

.. code-block:: yaml+jinja

    - name: Gather ID Information for connector Enrollement Certificate
      willguibr.zpacloud_ansible.zpa_enrollement_certificate_info:
        name: "Connector"
      register: connector_cert_id

    - debug:
        msg: "{{ connector_cert_id.data[0].id }}"

    - name: Gather ID Information for an App Connector Group
      willguibr.zpacloud_ansible.zpa_app_connector_groups_info:
        name: "Example"
      register: app_connector_id

    - debug:
        msg: "{{ app_connector_id.data[0].id }}"

    - name: Create/Update/Delete an App Connector Group Provisioning Key
      willguibr.zpacloud_ansible.zpa_provisioning_key:
        name: "App Connector Group Provisioning Key"
        association_type: "CONNECTOR_GRP"
        max_usage: "10"
        enrollment_cert_id: "{{ connector_cert_id.data[0].id }}"
        zcomponent_id: "{{ app_connector_group.data[0].id }}"


.. code-block:: yaml+jinja

    - name: Gather ID Information for Service Edge Enrollement Certificate
      willguibr.zpacloud_ansible.zpa_enrollement_certificate_info:
        name: "Service Edge"
      register: service_edge_cert_id

    - debug:
        msg: "{{ service_edge_cert_id.data[0].id }}"

    - name: Gather ID Information for a Service Edge Group
      willguibr.zpacloud_ansible.zpa_service_edge_groups_info:
        name: "Example"
      register: service_edge_group_id

    - debug:
        msg: "{{ service_edge_group_id.data[0].id }}"

    - name: Create/Update/Delete an App Connector Group Provisioning Key
      willguibr.zpacloud_ansible.zpa_provisioning_key:
        name: "App Connector Group Provisioning Key"
        association_type: "CONNECTOR_GRP"
        max_usage: "10"
        enrollment_cert_id: "{{ service_edge_cert_id.data[0].id }}"
        zcomponent_id: "{{ service_edge_group_id.data[0].id }}"


Status
------
N/A


Authors
~~~~~~~

- William Guilherme (@willguibr)