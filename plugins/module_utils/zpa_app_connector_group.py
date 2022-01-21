import re
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper, delete_none,camelcaseToSnakeCase
)


class AppConnectorGroupService:
    def __init__(self, module, customer_id):
        self.module = module
        self.customer_id = customer_id
        self.rest = ZPAClientHelper(module)

    def getByIDOrName(self, id, name):
        app = None
        if id is not None:
            app = self.getByID(id)
        if app is None and name is not None:
            app = self.getByName(name)
        return app

    def getByID(self, id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/appConnectorGroup/%s" % (self.customer_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAll(self):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v1/admin/customers/%s/appConnectorGroup" % (self.customer_id), data_key_name="list")
        apps = []
        for app in list:
            apps.append(self.mapRespJSONToApp(app))
        return apps

    def getByName(self, name):
        apps = self.getAll()
        for app in apps:
            if app.get("name") == name:
                return app
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
            "connectors": self.mapConnectorsJSONToList(resp_json.get("connectors")),
            "id": resp_json.get("id"),
            "name": resp_json.get("name"),
            "description": resp_json.get("description"),
            "enabled": resp_json.get("enabled"),
            "city_country": resp_json.get("cityCountry"),
            "country_code": resp_json.get("countryCode"),
            "latitude": resp_json.get("latitude"),
            "longitude": resp_json.get("longitude"),
            "location": resp_json.get("location"),
            "upgrade_day": resp_json.get("upgradeDay"),
            "upgrade_time_in_secs": resp_json.get("upgradeTimeInSecs"),
            "override_version_profile": resp_json.get("overrideVersionProfile"),
            "version_profile_id": resp_json.get("versionProfileId"),
            "dns_query_type": resp_json.get("dnsQueryType"),
        }

    @delete_none
    def mapAppToJSON(self, app):
        if app is None:
            return {}
        return {
            "connectors": self.mapConnectorsListToJSON(app.get("connectors")),
            "id": app.get("id"),
            "name": app.get("name"),
            "description": app.get("description"),
            "enabled": app.get("enabled"),
            "cityCountry": app.get("city_country"),
            "countryCode": app.get("country_code"),
            "latitude": app.get("latitude"),
            "longitude": app.get("longitude"),
            "location": app.get("location"),
            "upgradeDay": app.get("upgrade_day"),
            "upgradeTimeInSecs": app.get("upgrade_time_in_secs"),
            "overrideVersionProfile": app.get("override_version_profile"),
            "versionProfileId": app.get("version_profile_id"),
            "dnsQueryType": app.get("dns_query_type"),
        }

    def create(self, app):
        """Create new AppConnectorGroup"""
        appJSON = self.mapAppToJSON(app)
        response = self.rest.post(
            "/mgmtconfig/v1/admin/customers/%s/appConnectorGroup" % (self.customer_id), data=appJSON)
        status_code = response.status_code
        if status_code > 299:
            return None
        return self.mapRespJSONToApp(response.json)

    def update(self, app):
        """update the AppConnectorGroup"""
        appJSON = self.mapAppToJSON(app)
        response = self.rest.put(
            "/mgmtconfig/v1/admin/customers/%s/appConnectorGroup/%s" % (self.customer_id, appJSON.get("id")), data=appJSON)
        status_code = response.status_code
        if status_code > 299:
            return None
        return app

    def delete(self, id):
        """delete the AppConnectorGroup"""
        response = self.rest.delete(
            "/mgmtconfig/v1/admin/customers/%s/appConnectorGroup/%s" % (self.customer_id, id))
        return response.status_code
