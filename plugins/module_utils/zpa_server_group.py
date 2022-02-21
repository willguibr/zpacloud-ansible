from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re

from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    camelcaseToSnakeCase,
    delete_none,
)


class ServerGroupService:
    def __init__(self, module, customer_id, rest):
        self.module = module
        self.customer_id = customer_id
        self.rest = rest

    def getByIDOrName(self, id, name):
        server_group = None
        if id is not None:
            server_group = self.getByID(id)
        if server_group is None and name is not None:
            server_group = self.getByName(name)
        return server_group

    def getByID(self, id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/serverGroup/%s" % (self.customer_id, id)
        )
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAll(self):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v1/admin/customers/%s/serverGroup"
            % (self.customer_id),
            data_key_name="list",
        )
        server_groups = []
        for server_group in list:
            server_groups.append(self.mapRespJSONToApp(server_group))
        return server_groups

    def getByName(self, name):
        server_groups = self.getAll()
        for server_group in server_groups:
            if server_group.get("name") == name:
                return server_group
        return None

    def mapListJSONToList(self, entities):
        if entities is None:
            return []
        l = []
        for s in entities:
            l.append(camelcaseToSnakeCase(s))
        return l

    def mapListToJSONList(self, entities):
        if entities is None:
            return []
        l = []
        for e in entities:
            l.append(dict(id=e.get("id")))
        return l

    @delete_none
    def mapRespJSONToApp(self, resp_json):
        if resp_json is None:
            return {}
        return {
            "id": resp_json.get("id"),
            "name": resp_json.get("name"),
            "description": resp_json.get("description"),
            "enabled": resp_json.get("enabled"),
            "ip_anchored": resp_json.get("ipAnchored"),
            "config_space": resp_json.get("configSpace"),
            "dynamic_discovery": resp_json.get("dynamicDiscovery"),
            "servers": self.mapListJSONToList(resp_json.get("servers")),
            "applications": self.mapListJSONToList(resp_json.get("applications")),
            "app_connector_groups": self.mapListJSONToList(
                resp_json.get("appConnectorGroups")
            ),
        }

    @delete_none
    def mapAppToJSON(self, server_group):
        if server_group is None:
            return {}
        return {
            "id": server_group.get("id"),
            "name": server_group.get("name"),
            "description": server_group.get("description"),
            "enabled": server_group.get("enabled"),
            "ipAnchored": server_group.get("ip_anchored"),
            "configSpace": server_group.get("config_space"),
            "dynamicDiscovery": server_group.get("dynamic_discovery"),
            "servers": self.mapListToJSONList(server_group.get("servers")),
            "applications": self.mapListToJSONList(server_group.get("applications")),
            "appConnectorGroups": self.mapListToJSONList(
                server_group.get("app_connector_groups")
            ),
        }

    def create(self, server_group):
        """Create new Server Group"""
        serverGroupJson = self.mapAppToJSON(server_group)
        response = self.rest.post(
            "/mgmtconfig/v1/admin/customers/%s/serverGroup" % (self.customer_id),
            data=serverGroupJson,
        )
        status_code = response.status_code
        if status_code > 299:
            return None
        return self.getByID(response.json.get("id"))

    def update(self, server_group):
        """update the Server Group"""
        serverGroupJson = self.mapAppToJSON(server_group)
        response = self.rest.put(
            "/mgmtconfig/v1/admin/customers/%s/serverGroup/%s"
            % (self.customer_id, serverGroupJson.get("id")),
            data=serverGroupJson,
        )
        status_code = response.status_code
        if status_code > 299:
            return None
        return self.getByID(serverGroupJson.get("id"))

    def delete(self, id):
        """delete the Server Group"""
        response = self.rest.delete(
            "/mgmtconfig/v1/admin/customers/%s/serverGroup/%s" % (self.customer_id, id)
        )
        return response.status_code
