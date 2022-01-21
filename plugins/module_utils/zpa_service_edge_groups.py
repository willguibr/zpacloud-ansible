import re
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper, delete_none, camelcaseToSnakeCase
)


class ServiceEdgeGroupService:
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
            "/mgmtconfig/v1/admin/customers/%s/serviceEdgeGroup/%s" % (self.customer_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAll(self):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v1/admin/customers/%s/serviceEdgeGroup" % (self.customer_id), data_key_name="list")
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

    def mapServiceEdgesJSONToList(self, serviceEdges):
        if serviceEdges is None:
            return []
        l = []
        for s in serviceEdges:
            d = camelcaseToSnakeCase(s)
            l.append(d)
        return l

    def mapServiceEdgesListToJSON(self, serviceEdges):
        if serviceEdges is None:
            return []
        l = []
        for s in serviceEdges:
            d = dict(id=s.get("id"))
            l.append(d)
        return l

    def mapTrustedNetworksJSONToList(self, trustedNetworks):
        if trustedNetworks is None:
            return []
        l = []
        for app in trustedNetworks:
            d = camelcaseToSnakeCase(app)
            l.append(d)
        return l

    def mapTrustedNetworksListToJSON(self, trustedNetworks):
        if trustedNetworks is None:
            return []
        l = []
        for s in trustedNetworks:
            d = dict(id=s.get("id"))
            l.append(d)
        return l

    @delete_none
    def mapRespJSONToApp(self, resp_json):
        if resp_json is None:
            return {}
        return {
            "city_country": resp_json.get("cityCountry"),
            "country_code": resp_json.get("countryCode"),
            "description": resp_json.get("description"),
            "enabled": resp_json.get("enabled"),
            "geolocation_id": resp_json.get("geoLocationId"),
            "id": resp_json.get("id"),
            "is_public": resp_json.get("isPublic"),
            "latitude": resp_json.get("latitude"),
            "location": resp_json.get("location"),
            "longitude": resp_json.get("longitude"),
            "name": resp_json.get("name"),
            "override_version_profile": resp_json.get("overrideVersionProfile"),
            "upgrade_day": resp_json.get("upgradeDay"),
            "upgrade_time_in_secs": resp_json.get("upgradeTimeInSecs"),
            "version_profile_id": resp_json.get("versionProfileId"),
            "version_profile_name": resp_json.get("versionProfileName"),
            "version_profile_visibility_scope": resp_json.get("versionProfileVisibilityScope"),
            "service_edges": self.mapServiceEdgesJSONToList(resp_json.get("serviceEdges")),
            "trusted_networks": self.mapTrustedNetworksJSONToList(resp_json.get("trustedNetworks")),
        }

    @delete_none
    def mapAppToJSON(self, serviceEdge):
        if serviceEdge is None:
            return {}
        return {
            "cityCountry": serviceEdge.get("city_country"),
            "countryCode": serviceEdge.get("country_code"),
            "description": serviceEdge.get("description"),
            "enabled": serviceEdge.get("enabled"),
            "geoLocationId": serviceEdge.get("geolocation_id"),
            "id": serviceEdge.get("id"),
            "isPublic": serviceEdge.get("is_public"),
            "latitude": serviceEdge.get("latitude"),
            "location": serviceEdge.get("location"),
            "longitude": serviceEdge.get("longitude"),
            "name": serviceEdge.get("name"),
            "overrideVersionProfile": serviceEdge.get("override_version_profile"),
            "upgradeDay": serviceEdge.get("upgrade_day"),
            "upgradeTimeInSecs": serviceEdge.get("upgrade_time_in_secs"),
            "versionProfileId": serviceEdge.get("version_profile_id"),
            "versionProfileVisibilityScope": serviceEdge.get("version_profile_visibility_scope"),
            "serviceEdges": self.mapServiceEdgesListToJSON(serviceEdge.get("service_edges")),
            "trustedNetworks": self.mapTrustedNetworksListToJSON(serviceEdge.get("trusted_networks")),
        }

    def create(self, app):
        """Create new ServiceEdgeGroup"""
        appJSON = self.mapAppToJSON(app)
        response = self.rest.post(
            "/mgmtconfig/v1/admin/customers/%s/serviceEdgeGroup" % (self.customer_id), data=appJSON)
        status_code = response.status_code
        if status_code > 299:
            return None
        return self.mapRespJSONToApp(response.json)

    def update(self, app):
        """update the ServiceEdgeGroup"""
        appJSON = self.mapAppToJSON(app)
        response = self.rest.put(
            "/mgmtconfig/v1/admin/customers/%s/serviceEdgeGroup/%s" % (self.customer_id, appJSON.get("id")), data=appJSON)
        status_code = response.status_code
        if status_code > 299:
            return None
        return app

    def delete(self, id):
        """delete the ServiceEdgeGroup"""
        response = self.rest.delete(
            "/mgmtconfig/v1/admin/customers/%s/serviceEdgeGroup/%s" % (self.customer_id, id))
        return response.status_code
