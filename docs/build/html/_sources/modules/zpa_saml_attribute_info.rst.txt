.. _zpa_saml_attribute_info_module:


zpa_saml_attribute_info - Get details (ID and/or Name) of SAML Attribute.
=========================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module retrieves details of a SAML Attribute in the ZPA Cloud, so it can be used
in access policy, timeout policy, or forwarding policy.




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

            The name of saml attribute.

      id (str):

         The unique identifier for the saml attribute.


Notes
-----

Examples
--------

.. code-block:: yaml+jinja

      - name: Gather Information about all SAML Attribute
         willguibr.zpacloud.zpa_saml_attribute_info:
         register: all_saml_attributes

      - debug:
         msg: "{{ all_saml_attributes }}"

      - name: Gather information about all SAML Attribute
         willguibr.zpacloud.zpa_saml_attribute_info:
            name: DepartmentName
         register: saml_attribute_name

      - debug:
         msg: "{{ saml_attribute_name.data[0].id }}"

      - name: Gather information about all SAML Attribute
         willguibr.zpacloud.zpa_saml_attribute_info:
            id: 216196257331282234
         register: saml_attribute_id

      - debug:
         msg: "{{ saml_attribute_id }}"




Status
------
N/A


Authors
~~~~~~~

- William Guilherme (@willguibr)