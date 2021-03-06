from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re

from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper,
    camelcaseToSnakeCase,
    delete_none,
)


class ProfileVersionService:
    def __init__(self, module, customer_id):
        self.module = module
        self.customer_id = customer_id
        self.rest = ZPAClientHelper(module)

    def getByIDOrName(self, id, name):
        version = None
        if id is not None:
            version = self.getByID(id)
        if version is None and name is not None:
            version = self.getByName(name)
        return version

    def getByID(self, id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/visible/versionProfiles/%s"
            % (self.customer_id, id)
        )
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAll(self):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v1/admin/customers/%s/visible/versionProfiles"
            % (self.customer_id),
            data_key_name="list",
        )
        networks = []
        for network in list:
            networks.append(self.mapRespJSONToApp(network))
        return networks

    def getByName(self, name):
        networks = self.getAll()
        for network in networks:
            if network.get("name") == name:
                return network
        return None

    def mapJSONCustomScopeCustomerIds(self, d):
        if d is None:
            return None
        scopes = []
        for v in d:
            scopes.append(camelcaseToSnakeCase(v))
        return scopes

    def mapJSONCustomScopeRequestCustomerIds(self, d):
        if d is None:
            return None
        return camelcaseToSnakeCase(d)

    def mapJSONVersions(self, d):
        if d is None:
            return None
        versions = []
        for v in d:
            versions.append(camelcaseToSnakeCase(v))
        return versions

    @delete_none
    def mapRespJSONToApp(self, resp_json):
        if resp_json is None:
            return {}
        return {
            "creation_time": resp_json.get("creationTime"),
            "customer_id": resp_json.get("customerId"),
            "description": resp_json.get("description"),
            "id": resp_json.get("id"),
            "modified_by": resp_json.get("modifiedBy"),
            "modified_time": resp_json.get("modifiedTime"),
            "name": resp_json.get("name"),
            "upgrade_priority": resp_json.get("upgradePriority"),
            "visibility_scope": resp_json.get("visibilityScope"),
            "custom_scope_request_customer_ids": self.mapJSONCustomScopeRequestCustomerIds(
                resp_json.get("customScopeRequestCustomerIds")
            ),
            "custom_scope_customer_ids": self.mapJSONCustomScopeCustomerIds(
                resp_json.get("customScopeCustomerIds")
            ),
            "versions": self.mapJSONVersions(resp_json.get("versions")),
        }
