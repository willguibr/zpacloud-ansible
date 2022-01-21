import re
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper, delete_none, camelcaseToSnakeCase, snakecaseToCamelcase
)


class BrowserAccessService:
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
            "/mgmtconfig/v1/admin/customers/%s/application/%s" % (self.customer_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAll(self):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v1/admin/customers/%s/application" % (self.customer_id), data_key_name="list")
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

    def mapServerGroupsJSONToList(self, serverGroups):
        if serverGroups is None:
            return []
        l = []
        for s in serverGroups:
            d = camelcaseToSnakeCase(s)
            l.append(d)
        return l


    def mapServerGroupsListToJSON(self, serverGroups):
        if serverGroups is None:
            return []
        l = []
        for s in serverGroups:
            d = dict(id=s.get("id"))
            l.append(d)
        return l

    def mapClientlessAppsJSONToList(self, apps):
        if apps is None:
            return []
        l = []
        for app in apps:
            d = camelcaseToSnakeCase(app)
            l.append(d)
        return l

    def mapClientlessAppsToJSONList(self, apps):
        if apps is None:
            return []
        l = []
        for app in apps:
            d = snakecaseToCamelcase(app)
            l.append(d)
        return l

    @delete_none
    def mapRespJSONToApp(self, resp_json):
        if resp_json is None:
            return {}
        return {
            "segment_group_id": resp_json.get("segmentGroupId"),
            "segment_group_name": resp_json.get("segmentGroupName"),
            "bypass_type": resp_json.get("bypassType"),
            "clientless_apps": self.mapClientlessAppsJSONToList(resp_json.get("clientlessApps")),
            "config_space": resp_json.get("configSpace"),
            "creation_time": resp_json.get("creationTime"),
            "default_idle_timeout": resp_json.get("defaultIdleTimeout"),
            "default_max_age": resp_json.get("defaultMaxAge"),
            "description": resp_json.get("description"),
            "domain_names": resp_json.get("domainNames"),
            "double_encrypt": resp_json.get("doubleEncrypt"),
            "enabled": resp_json.get("enabled"),
            "health_check_type": resp_json.get("healthCheckType"),
            "health_reporting": resp_json.get("healthReporting"),
            "icmp_access_type": resp_json.get("icmpAccessType"),
            "id": resp_json.get("id"),
            "ip_anchored": resp_json.get("ipAnchored"),
            "is_cname_enabled": resp_json.get("isCnameEnabled"),
            "modified_by": resp_json.get("modifiedBy"),
            "modified_time": resp_json.get("modifiedTime"),
            "name": resp_json.get("name"),
            "passive_health_enabled": resp_json.get("passiveHealthEnabled"),
            "tcp_port_range": resp_json.get("tcpPortRange"),
            "udp_port_range": resp_json.get("udpPortRange"),
            "server_groups": self.mapServerGroupsJSONToList(resp_json.get("serverGroups")),
        }

    @delete_none
    def mapAppToJSON(self, app):
        if app is None:
            return {}
        return {
            "segmentGroupId": app.get("segment_group_id"),
            "segmentGroupName": app.get("segment_group_name"),
            "bypassType": app.get("bypass_type"),
            "configSpace": app.get("config_space"),
            "creationTime": app.get("creation_time"),
            "defaultIdleTimeout": app.get("default_idle_timeout"),
            "defaultMaxAge": app.get("default_max_age"),
            "description": app.get("description"),
            "domainNames": app.get("domain_names"),
            "doubleEncrypt": app.get("double_encrypt"),
            "enabled": app.get("enabled"),
            "healthCheckType": app.get("health_check_type"),
            "healthReporting": app.get("health_reporting"),
            "icmpAccessType": app.get("icmp_access_type"),
            "id": app.get("id"),
            "ipAnchored": app.get("ip_anchored"),
            "isCnameEnabled": app.get("is_cname_enabled"),
            "modifiedBy": app.get("modified_by"),
            "modifiedTime": app.get("modified_time"),
            "name": app.get("name"),
            "passiveHealthEnabled": app.get("passive_health_enabled"),
            "tcpPortRange": app.get("tcp_port_range"),
            "udpPortRange": app.get("udp_port_range"),
            "serverGroups": self.mapServerGroupsListToJSON(app.get("server_groups")),
            "clientlessApps": self.mapClientlessAppsToJSONList(app.get("clientless_apps")),
        }

    def create(self, app):
        """Create new application"""
        appJSON = self.mapAppToJSON(app)
        response = self.rest.post(
            "/mgmtconfig/v1/admin/customers/%s/application" % (self.customer_id), data=appJSON)
        status_code = response.status_code
        if status_code > 299:
            return None
        return self.getByID(response.json.get("id"))

    def update(self, app):
        """update the application"""
        appJSON = self.mapAppToJSON(app)
        response = self.rest.put(
            "/mgmtconfig/v1/admin/customers/%s/application/%s" % (self.customer_id, appJSON.get("id")), data=appJSON)
        status_code = response.status_code
        if status_code > 299:
            return None
        return self.getByID(appJSON.get("id"))

    def detach_from_segment_group(self, app_id, seg_group_id):
        seg_group = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/segmentGroup/%s" % (self.customer_id, seg_group_id))
        if seg_group.status_code > 299:
            return None
        data = seg_group.json
        apps = data.get("applications", [])
        addaptedApps = []
        for app in apps:
            if app.get("id") != app_id:
                addaptedApps.append(app)
        data["applications"] = addaptedApps
        self.rest.put(
            "/mgmtconfig/v1/admin/customers/%s/segmentGroup/%s" % (self.customer_id, seg_group_id), data=data)

    def delete(self, id):
        """delete the application"""
        response = self.rest.delete(
            "/mgmtconfig/v1/admin/customers/%s/application/%s" % (self.customer_id, id))
        return response.status_code
