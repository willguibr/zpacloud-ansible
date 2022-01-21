from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper, delete_none
)
import re


class ProvisioningKeyService:
    def __init__(self, module, customer_id):
        self.module = module
        self.customer_id = customer_id
        self.rest = ZPAClientHelper(module)
        self.association_types = ["CONNECTOR_GRP", "SERVICE_EDGE_GRP"]

    def getByIDOrName(self, id, name, association_type):
        provisioning_key = None
        if id is not None:
            provisioning_key = self.getByID(id, association_type)
        if provisioning_key is None and name is not None:
            provisioning_key = self.getByName(name, association_type)
        return provisioning_key

    def getByID(self, id, association_type):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/associationType/%s/provisioningKey/%s" % (self.customer_id, association_type, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAll(self, association_type):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v1/admin/customers/%s/associationType/%s/provisioningKey" % (self.customer_id, association_type), data_key_name="list")
        provisioning_keys = []
        for provisioning_key in list:
            provisioning_keys.append(self.mapRespJSONToApp(provisioning_key))
        return provisioning_keys

    def getByNameAllAssociations(self, name):
        for assoc_type in self.association_types:
            pro_key = self.getByName(name, assoc_type)
            if pro_key is not None:
                return pro_key
            return None

    def getByIDAllAssociations(self, id):
        for assoc_type in self.association_types:
            pro_key = self.getByID(id, assoc_type)
            if pro_key is not None:
                return pro_key
            return None

    def getByName(self, name, association_type):
        provisioning_keys = self.getAll(association_type)
        for provisioning_key in provisioning_keys:
            if provisioning_key.get("name") == name:
                return provisioning_key
        return None

    @delete_none
    def mapRespJSONToApp(self, resp_json):
        if resp_json is None:
            return {}
        return {
            "app_connector_group_id": resp_json.get("appConnectorGroupId"),
            "app_connector_group_name": resp_json.get("appConnectorGroupName"),
            "creation_time": resp_json.get("creationTime"),
            "enabled": resp_json.get("enabled"),
            "expiration_in_epoch_sec": resp_json.get("expirationInEpochSec"),
            "id": resp_json.get("id"),
            "ip_acl": resp_json.get("ipAcl"),
            "max_usage": resp_json.get("maxUsage"),
            "modified_by": resp_json.get("modifiedBy"),
            "modified_time": resp_json.get("modifiedTime"),
            "name": resp_json.get("name"),
            "provisioning_key": resp_json.get("provisioningKey"),
            "enrollment_cert_id": resp_json.get("enrollmentCertId"),
            "enrollment_cert_name": resp_json.get("enrollmentCertName"),
            "ui_config": resp_json.get("uiConfig"),
            "usage_count": resp_json.get("usageCount"),
            "zcomponent_id": resp_json.get("zcomponentId"),
            "zcomponent_name": resp_json.get("zcomponentName"),
        }

    @delete_none
    def mapAppToJSON(self, provisioning_key):
        if provisioning_key is None:
            return {}
        return {
            "appConnectorGroupId": provisioning_key.get("app_connector_group_id"),
            "appConnectorGroupName": provisioning_key.get("app_connector_group_name"),
            "creationTime": provisioning_key.get("creation_time"),
            "enabled": provisioning_key.get("enabled"),
            "expirationInEpochSec": provisioning_key.get("expiration_in_epoch_sec"),
            "id": provisioning_key.get("id"),
            "ipAcl": provisioning_key.get("ip_acl"),
            "maxUsage": provisioning_key.get("max_usage"),
            "modifiedBy": provisioning_key.get("modified_by"),
            "modifiedTime": provisioning_key.get("modified_time"),
            "name": provisioning_key.get("name"),
            "provisioningKey": provisioning_key.get("provisioning_key"),
            "enrollmentCertId": provisioning_key.get("enrollment_cert_id"),
            "enrollmentCertName": provisioning_key.get("enrollment_cert_name"),
            "uiConfig": provisioning_key.get("ui_config"),
            "usageCount": provisioning_key.get("usage_count"),
            "zcomponentId": provisioning_key.get("zcomponent_id"),
            "zcomponentName": provisioning_key.get("zcomponent_name"),
        }

    def create(self, provisioning_key, association_type):
        """Create new Provisioning Key"""
        provisioningKeyJson = self.mapAppToJSON(provisioning_key)
        response = self.rest.post(
            "/mgmtconfig/v1/admin/customers/%s/associationType/%s/provisioningKey" % (self.customer_id, association_type), data=provisioningKeyJson)
        status_code = response.status_code
        if status_code > 299:
            return None
        return self.getByID(response.json.get("id"), association_type)

    def update(self, provisioning_key, association_type):
        """update the Provisioning Key"""
        provisioningKeyJson = self.mapAppToJSON(provisioning_key)
        response = self.rest.put(
            "/mgmtconfig/v1/admin/customers/%s/associationType/%s/provisioningKey/%s" % (self.customer_id, association_type, provisioningKeyJson.get("id")), data=provisioningKeyJson)
        status_code = response.status_code
        if status_code > 299:
            return None
        return self.getByID(provisioningKeyJson.get("id"), association_type)

    def delete(self, id, association_type):
        """delete the Provisioning Key"""
        response = self.rest.delete(
            "/mgmtconfig/v1/admin/customers/%s/associationType/%s/provisioningKey/%s" % (self.customer_id, association_type, id))
        return response.status_code
