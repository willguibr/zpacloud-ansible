import re
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper, delete_none,camelcaseToSnakeCase
)


class AppConnectorControllerService:
    def __init__(self, module, customer_id):
        self.module = module
        self.customer_id = customer_id
        self.rest = ZPAClientHelper(module)

    def getByIDOrName(self, id, name):
        connector = None
        if id is not None:
            connector = self.getByID(id)
        if connector is None and name is not None:
            connector = self.getByName(name)
        return connector

    def getByID(self, id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/connector/%s" % (self.customer_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAll(self):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v1/admin/customers/%s/connector" % (self.customer_id), data_key_name="list")
        connectors = []
        for connector in list:
            connectors.append(self.mapRespJSONToApp(connector))
        return connectors

    def getByName(self, name):
        connectors = self.getAll()
        for connector in connectors:
            if connector.get("name") == name:
                return connector
        return None

    def mapConnectorsJSONToList(self, connectors):
        if connectors is None:
            return []
        l = []
        for s in connectors:
            d = camelcaseToSnakeCase(s)
            l.append(d)
        return l

    def mapConnectorsListToJSON(self, connectors):
        if connectors is None:
            return []
        l = []
        for s in connectors:
            d = dict(id=s.get("id"))
            l.append(d)
        return l

    @delete_none
    def mapRespJSONToApp(self, resp_json):
        if resp_json is None:
            return {}
        return {
            # "connectors": self.mapConnectorsJSONToList(resp_json.get("connectors")),
            "application_start_time": resp_json.get("applicationStartTime"),
            "app_connector_group_id": resp_json.get("appConnectorGroupId"),
            "app_connector_group_name": resp_json.get("appConnectorGroupName"),
            "control_channel_status": resp_json.get("controlChannelStatus"),
            "creation_time": resp_json.get("creationTime"),
            "country_code": resp_json.get("countryCode"),
            "ctrl_broker_name": resp_json.get("ctrlBrokerName"),
            "current_version": resp_json.get("currentVersion"),
            "description": resp_json.get("description"),
            "enabled": resp_json.get("enabled"),
            "expected_upgrade_time": resp_json.get("expectedUpgradeTime"),
            "expected_version": resp_json.get("expectedVersion"),
            "fingerprint": resp_json.get("fingerprint"),
            "id": resp_json.get("id"),
            "ip_acl": resp_json.get("ipAcl"),
            "issued_cert_id": resp_json.get("issuedCertId"),
            "last_broker_connect_time": resp_json.get("lastBrokerConnectTime"),
            "last_broker_connect_time_duration": resp_json.get("lastBrokerConnectTimeDuration"),
            "last_broker_disconnect_time": resp_json.get("lastBrokerDisconnectTime"),
            "last_broker_disconnect_time_duration": resp_json.get("lastBrokerDisconnectTimeDuration"),
            "last_upgrade_time": resp_json.get("lastUpgradeTime"),
            "latitude": resp_json.get("latitude"),
            "location": resp_json.get("location"),
            "longitude": resp_json.get("longitude"),
            "modified_by": resp_json.get("modifiedBy"),
            "modified_time": resp_json.get("modifiedTime"),
            "name": resp_json.get("name"),
            "provisioning_key_id": resp_json.get("provisioningKeyId"),
            "provisioning_key_name": resp_json.get("provisioningKeyName"),
            "platform": resp_json.get("platform"),
            "previous_version": resp_json.get("previousVersion"),
            "private_ip": resp_json.get("privateIp"),
            "public_ip": resp_json.get("c"),
            "sarge_version": resp_json.get("sargeVersion"),
            "enrollment_cert": resp_json.get("enrollmentCert"),
            "upgrade_attempt": resp_json.get("upgradeAttempt"),
            "upgrade_status": resp_json.get("upgradeStatus"),
        }

    @delete_none
    def mapAppToJSON(self, connector):
        if connector is None:
            return {}
        return {
            # "connectors": self.mapConnectorsListToJSON(connector.get("connectors")),
            "applicationStartTime": connector.get("application_start_time"),
            "appConnectorGroupId": connector.get("app_connector_group_id"),
            "appConnectorGroupName": connector.get("app_connector_group_name"),
            "controlChannelStatus": connector.get("control_channel_status"),
            "creationTime": connector.get("creation_time"),
            "countryCode": connector.get("country_code"),
            "ctrlBrokerName": connector.get("ctrl_broker_name"),
            "currentVersion": connector.get("current_version"),
            "description": connector.get("description"),
            "enabled": connector.get("enabled"),
            "expectedUpgradeTime": connector.get("expected_upgrade_time"),
            "expectedVersion": connector.get("expected_version"),
            "fingerprint": connector.get("fingerprint"),
            "id": connector.get("id"),   
            "ipAcl": connector.get("ip_acl"),
            "issuedCertId": connector.get("issued_cert_id"),
            "lastBrokerConnectTime": connector.get("last_broker_connect_time"),
            "lastBrokerConnectTimeDuration": connector.get("last_broker_connect_time_duration"),
            "lastBrokerDisconnectTime": connector.get("last_broker_disconnect_time"),
            "lastBrokerDisconnectTimeDuration": connector.get("last_broker_disconnect_time_duration"), 
            "lastUpgradeTime": connector.get("last_upgrade_time"),
            "latitude": connector.get("latitude"),
            "location": connector.get("location"),
            "longitude": connector.get("longitude"),
            "modifiedBy": connector.get("modified_by"),
            "modifiedTime": connector.get("modified_time"),
            "name": connector.get("name"),
            "provisioningKeyId": connector.get("provisioning_key_id"),
            "provisioningKeyName": connector.get("provisioning_key_name"),
            "platform": connector.get("platform"),
            "previousVersion": connector.get("previous_version"),
            "privateIp": connector.get("private_ip"),
            "publicIp": connector.get("public_ip"),
            "sargeVersion": connector.get("sarge_version"),
            "enrollmentCert": connector.get("enrollment_cert"),
            "upgradeAttempt": connector.get("upgrade_attempt"),
            "upgradeStatus": connector.get("upgrade_status"),
        }

    def bulkDelete(self, app):
        """Bulk Delete App Connectors"""
        appJSON = self.mapAppToJSON(app)
        response = self.rest.post(
            "/mgmtconfig/v1/admin/customers/%s/connector/bulkDelete" % (self.customer_id), data=appJSON)
        status_code = response.status_code
        if status_code > 299:
            return None
        return self.mapRespJSONToApp(response.json)

    def update(self, app):
        """update the App Connectors"""
        appJSON = self.mapAppToJSON(app)
        response = self.rest.put(
            "/mgmtconfig/v1/admin/customers/%s/connector/%s" % (self.customer_id, appJSON.get("id")), data=appJSON)
        status_code = response.status_code
        if status_code > 299:
            return None
        return app

    def delete(self, id):
        """delete the App Connectors"""
        response = self.rest.delete(
            "/mgmtconfig/v1/admin/customers/%s/connector/%s" % (self.customer_id, id))
        return response.status_code
