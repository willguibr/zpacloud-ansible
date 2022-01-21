from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper, delete_none
)


class CloudConnectorGroupService:
    def __init__(self, module, customer_id):
        self.module = module
        self.customer_id = customer_id
        self.rest = ZPAClientHelper(module)

    def getByIDOrName(self, id, name):
        cloud_connector = None
        if id is not None:
            cloud_connector = self.getByID(id)
        if cloud_connector is None and name is not None:
            cloud_connector = self.getByName(name)
        return cloud_connector

    def getByID(self, id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/cloudConnectorGroup/%s" % (self.customer_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAll(self):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v1/admin/customers/%s/cloudConnectorGroup" % (self.customer_id), data_key_name="list")
        cloud_connectors = []
        for app in list:
            cloud_connectors.append(self.mapRespJSONToApp(app))
        return cloud_connectors

    def getByName(self, name):
        cloud_connectors = self.getAll()
        for cloud_connector in cloud_connectors:
            if cloud_connector.get("name") == name:
                return cloud_connector
        return None

    @delete_none
    def mapRespJSONToApp(self, resp_json):
        if resp_json is None:
            return {}
        return {
            "creation_time": resp_json.get("creationTime"),
            "description": resp_json.get("description"),
            "cloud_connectors": resp_json.get("cloudConnectors"),
            "enabled": resp_json.get("enabled"),
            "geolocation_id": resp_json.get("geoLocationId"),
            "id": resp_json.get("id"),
            "modified_by": resp_json.get("modifiedBy"),
            "modified_time": resp_json.get("modifiedTime"),
            "name": resp_json.get("name"),
            "zia_cloud": resp_json.get("ziaCloud"),
            "zia_org_id": resp_json.get("ziaOrgId"),
        }

    @delete_none
    def mapAppToJSON(self, cloudConnector):
        if cloudConnector is None:
            return {}
        return {
            "creationTime": cloudConnector.get("creation_time"),
            "description": cloudConnector.get("description"),
            "cloudConnectors": cloudConnector.get("cloud_connectors"),
            "enabled": cloudConnector.get("enabled"),
            "geoLocationId": cloudConnector.get("geolocation_id"),
            "id": cloudConnector.get("id"),
            "modifiedBy": cloudConnector.get("modified_by"),
            "modifiedTime": cloudConnector.get("modified_time"),
            "name": cloudConnector.get("name"),
            "ziaCloud": cloudConnector.get("zia_cloud"),
            "ziaOrgId": cloudConnector.get("zia_org_id"),
        }
