from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper, delete_none, camelcaseToSnakeCase
)
import re


class SegmentGroupService:
    def __init__(self, module, customer_id):
        self.module = module
        self.customer_id = customer_id
        self.rest = ZPAClientHelper(module)

    def getByIDOrName(self, id, name):
        segment_group = None
        if id is not None:
            segment_group = self.getByID(id)
        if segment_group is None and name is not None:
            segment_group = self.getByName(name)
        return segment_group

    def getByID(self, id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/segmentGroup/%s" % (self.customer_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAll(self):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v1/admin/customers/%s/segmentGroup" % (self.customer_id), data_key_name="list")
        segment_groups = []
        for segment_group in list:
            segment_groups.append(self.mapRespJSONToApp(segment_group))
        return segment_groups

    def getByName(self, name):
        segment_groups = self.getAll()
        for segment_group in segment_groups:
            if segment_group.get("name") == name:
                return segment_group
        return None

    def mapListJSONToList(self, entities):
        if entities is None:
            return []
        l = []
        for s in entities:
            l.append(camelcaseToSnakeCase(s))
        return l

    def mapListToJSONObjList(self, entities):
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
            "applications": self.mapListJSONToList(resp_json.get("applications")),
            "config_space": resp_json.get("configSpace"),
            "description": resp_json.get("description"),
            "enabled": resp_json.get("enabled"),
            "id": resp_json.get("id"),
            "name": resp_json.get("name"),
            "policy_migrated": resp_json.get("policyMigrated"),
            "tcp_keep_alive_enabled": resp_json.get("tcpKeepAliveEnabled"),
        }
    @delete_none
    def mapAppToJSON(self, segment_group):
        if segment_group is None:
            return {}
        return {
            "applications": self.mapListToJSONObjList(segment_group.get("applications")),
            "configSpace": segment_group.get("config_space"),
            "description": segment_group.get("description"),
            "enabled": segment_group.get("enabled"),
            "id": segment_group.get("id"),
            "name": segment_group.get("name"),
            "policyMigrated": segment_group.get("policy_migrated"),
            "tcpKeepAliveEnabled": segment_group.get("tcp_keep_alive_enabled"),
        }

    def create(self, segment_group):
        """Create new Segment Group"""
        segmentGroupJson = self.mapAppToJSON(segment_group)
        response = self.rest.post(
            "/mgmtconfig/v1/admin/customers/%s/segmentGroup" % (self.customer_id), data=segmentGroupJson)
        status_code = response.status_code
        if status_code > 299:
            return None
        return self.getByID(response.json.get("id"))

    def update(self, segment_group):
        """update the Segment Group"""
        segmentGroupJson = self.mapAppToJSON(segment_group)
        response = self.rest.put(
            "/mgmtconfig/v1/admin/customers/%s/segmentGroup/%s" % (self.customer_id, segmentGroupJson.get("id")), data=segmentGroupJson)
        status_code = response.status_code
        if status_code > 299:
            return None
        return self.getByID(segmentGroupJson.get("id"))

    def delete(self, id):
        """delete the Segment Group"""
        response = self.rest.delete(
            "/mgmtconfig/v1/admin/customers/%s/segmentGroup/%s" % (self.customer_id, id))
        return response.status_code
