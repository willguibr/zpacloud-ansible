import re
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_client import (
    ZPAClientHelper,
)


class LSSConfigControllerService:
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
            "/mgmtconfig/v2/admin/customers/%s/lssConfig/%s" % (self.customer_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAll(self):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v2/admin/customers/%s/lssConfig" % (self.customer_id), data_key_name="list")
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
            d = self.camelcaseToSnakeCase(s)
            l.append(d)
        return l

    @staticmethod
    def camelcaseToSnakeCase(obj):
        new_obj = dict()
        for key, value in obj.items():
            if value is not None:
                new_obj[re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()] = value
        return new_obj

    def mapListJSONToList(self, entities):
        if entities is None:
            return []
        l = []
        for s in entities:
            l.append(self.camelcaseToSnakeCase(s))
        return l


    def mapConfigToListJSON(self, configJSON):
        configs = []
        for config in configJSON:
            configs.append({
                "auditMessage": config.get("audit_message"),
                "creationTime": config.get("creation_time"),
                "description": config.get("description"),
                "enabled": config.get("enabled"),
                "filter": config.get("filter"),
                "format": config.get("format"),
                "id": config.get("id"),
                "modifiedBy": config.get("modified_by"),
                "modifiedTime": config.get("modified_time"),
                "name": config.get("name"),
                "lssHost": config.get("lss_host"),
                "lssPort": config.get("lss_port"),
                "sourceLogType": config.get("source_log_type"),
                "useTls": config.get("use_tls"),
            })
        return configs
    
    def mapOperandsToList(self, operandsJSON):
        ops = []
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
        for cond in conditions:
            """"""
            conds.append({
                "operator": cond.get("operator"),
                "negated": cond.get("negated"),
                "operands": self.mapOperandsToListJSON(cond.get("operands")),
            })
        return conds
    
    def mapRespJSONToApp(self, resp_json):
        if resp_json is None:
            return {}
        return {
            "id": resp_json.get("id"),
            "config": self.mapConfigToListJSON(resp_json.get("config")),
            "connector_groups": self.mapListJSONToList(resp_json.get("connectorGroups")),
            "conditions": self.mapConditionsToList(resp_json.get("conditions")),
        }
    
    def mapAppToJSON(self, policy_rule):
        if policy_rule is None:
            return {}
        return self.delete_none({
            "id": policy_rule.get("id"),
            "config": policy_rule.get("config"),
            "connectorGroups": policy_rule.get("connector_groups"),
            "conditions": self.mapConditionsToJSONList(policy_rule.get("conditions")),
        })
    
    def create(self, app):
        """Create new LSSConfig"""
        appJSON = self.mapAppToJSON(app)
        response = self.rest.post(
            "/mgmtconfig/v2/admin/customers/%s/lssConfig" % (self.customer_id), data=appJSON)
        status_code = response.status_code
        if status_code > 299:
            return None
        return self.mapRespJSONToApp(response.json)

    def update(self, app):
        """update the LSSConfig"""
        appJSON = self.mapAppToJSON(app)
        response = self.rest.put(
            "/mgmtconfig/v2/admin/customers/%s/lssConfig/%s" % (self.customer_id, appJSON.get("id")), data=appJSON)
        status_code = response.status_code
        if status_code > 299:
            return None
        return app

    def delete(self, id):
        """delete the LSSConfig"""
        response = self.rest.delete(
            "/mgmtconfig/v2/admin/customers/%s/lssConfig/%s" % (self.customer_id, id))
        return response.status_code
