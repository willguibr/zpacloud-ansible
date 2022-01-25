import re
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper, delete_none, camelcaseToSnakeCase, snakecaseToCamelcase
)


class LSSConfigControllerService:
    def __init__(self, module, customer_id):
        self.module = module
        self.customer_id = customer_id
        self.rest = ZPAClientHelper(module)

    def getByIDOrName(self, id, name):
        lss_config = None
        if id is not None:
            lss_config = self.getByID(id)
        if lss_config is None and name is not None:
            lss_config = self.getByName(name)
        return lss_config

    def getByID(self, id):
        response = self.rest.get(
            "/mgmtconfig/v2/admin/customers/%s/lssConfig/%s" % (self.customer_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAll(self):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v2/admin/customers/%s/lssConfig" % (self.customer_id), data_key_name="list")
        lss_configs = []
        for lss_config in list:
            lss_configs.append(self.mapRespJSONToApp(lss_config))
        return lss_configs

    def getByName(self, name):
        lss_configs = self.getAll()
        for lss_config in lss_configs:
            if lss_config.get("config", {}).get("name") == name:
                return lss_config
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

    def mapOperandsToList(self, operandsJSON):
        ops = []
        if operandsJSON is None:
            return None
        for op in operandsJSON:
            ops.append({
                "id": op.get("id"),
                "creation_time": op.get("creationTime"),
                "modified_by": op.get("modifiedBy"),
                "object_type": op.get("objectType"),
                "lhs": op.get("lhs"),
                "rhs": op.get("rhs"),
                "name": op.get("name"),
            })
        return ops

    def mapOperandsToListJSON(self, operandsJSON):
        ops = []
        if operandsJSON is None:
            return None
        for op in operandsJSON:
            ops.append({
                "objectType": op.get("object_type"),
                "lhs": op.get("lhs"),
                "rhs": op.get("rhs"),
                "name": op.get("name"),
            })
        return ops

    def mapConditionsToList(self, conditionsJSON):
        conds = []
        if conditionsJSON is None:
            return None
        for cond in conditionsJSON:
            """"""
            conds.append({
                "id": cond.get("id"),
                "modified_time": cond.get("modifiedTime"),
                "creation_time": cond.get("creationTime"),
                "modified_by": cond.get("modifiedBy"),
                "operator": cond.get("operator"),
                "negated": cond.get("negated"),
                "operands": self.mapOperandsToList(cond.get("operands")),
            })
        return conds

    def mapConditionsToJSONList(self, conditions):
        conds = []
        if conditions is None:
            return None
        for cond in conditions:
            """"""
            conds.append({
                "operator": cond.get("operator"),
                "negated": cond.get("negated"),
                "operands": self.mapOperandsToListJSON(cond.get("operands")),
            })
        return conds

    @delete_none
    def mapRespJSONToApp(self, resp_json):
        if resp_json is None:
            return {}
        return {
            "id": resp_json.get("id"),
            "config": camelcaseToSnakeCase(resp_json.get("config")),
            "connector_groups": self.mapListJSONToList(resp_json.get("connectorGroups")),
            "conditions": self.mapConditionsToList(resp_json.get("conditions")),
        }

    @delete_none
    def mapAppToJSON(self, policy_rule):
        if policy_rule is None:
            return {}
        return {
            "id": policy_rule.get("id"),
            "config": snakecaseToCamelcase(policy_rule.get("config")),
            "connectorGroups": self.mapListToJSONList(policy_rule.get("connector_groups")),
            "conditions": self.mapConditionsToJSONList(policy_rule.get("conditions")),
        }

    def create(self, lss_config):
        """Create new LSSConfig"""
        appJSON = self.mapAppToJSON(lss_config)
        response = self.rest.post(
            "/mgmtconfig/v2/admin/customers/%s/lssConfig" % (self.customer_id), data=appJSON)
        status_code = response.status_code
        if status_code > 299:
            return None
        return self.mapRespJSONToApp(response.json)

    def update(self, lss_config):
        """update the LSSConfig"""
        appJSON = self.mapAppToJSON(lss_config)
        response = self.rest.put(
            "/mgmtconfig/v2/admin/customers/%s/lssConfig/%s" % (self.customer_id, appJSON.get("id")), data=appJSON)
        status_code = response.status_code
        if status_code > 299:
            return None
        return lss_config

    def delete(self, id):
        """delete the LSSConfig"""
        response = self.rest.delete(
            "/mgmtconfig/v2/admin/customers/%s/lssConfig/%s" % (self.customer_id, id))
        return response.status_code
