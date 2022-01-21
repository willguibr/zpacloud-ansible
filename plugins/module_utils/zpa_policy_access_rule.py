from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper, delete_none, camelcaseToSnakeCase
)
import re


class PolicyAccessRuleService:
    def __init__(self, module, customer_id):
        self.module = module
        self.customer_id = customer_id
        self.rest = ZPAClientHelper(module)

    def getByIDOrName(self, id, name, policy_set_id, policy_type):
        policy_rule = None
        if id is not None:
            policy_rule = self.getByID(id, policy_set_id)
        if policy_rule is None and name is not None:
            policy_rule = self.getByNameAndType(name, policy_type)
        return policy_rule

    def getByPolicyType(self, policyType):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/policySet/policyType/%s" % (self.customer_id, policyType))
        status_code = response.status_code
        if status_code != 200:
            return None
        return camelcaseToSnakeCase(response.json)

    def getByID(self, id, policy_set_id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/policySet/%s/rule/%s" % (self.customer_id, policy_set_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToPolicy(response.json)

    def getAllByPolicyType(self, policy_type):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v1/admin/customers/%s/policySet/rules/policyType/%s" % (self.customer_id, policy_type), data_key_name="list")
        policy_rules = []
        for policy_rule in list:
            policy_rules.append(self.mapRespJSONToPolicy(policy_rule))
        return policy_rules

    def getByNameAndType(self, name, type):
        policy_rules = self.getAllByPolicyType(type)
        for policy_rule in policy_rules:
            if policy_rule.get("name") == name:
                return policy_rule
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
        if conditionsJSON is None:
            return conds
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
            return conds
        for cond in conditions:
            """"""
            conds.append({
                "operator": cond.get("operator"),
                "negated": cond.get("negated"),
                "operands": self.mapOperandsToListJSON(cond.get("operands")),
            })
        return conds

    @delete_none
    def mapRespJSONToPolicy(self, resp_json):
        if resp_json is None:
            return {}
        return {
            "default_rule": resp_json.get("defaultRule"),
            "description": resp_json.get("description"),
            "policy_type": resp_json.get("policyType"),
            "custom_msg": resp_json.get("customMsg"),
            "policy_set_id": resp_json.get("policySetId"),
            "id": resp_json.get("id"),
            "reauth_default_rule": resp_json.get("reauthDefaultRule"),
            "lss_default_rule": resp_json.get("lssDefaultRule"),
            "bypass_default_rule": resp_json.get("reauthDefaultRule"),
            "reauth_idle_timeout": resp_json.get("reauthIdleTimeout"),
            "reauth_timeout": resp_json.get("reauthTimeout"),
            "action_id": resp_json.get("actionId"),
            "name": resp_json.get("name"),
            "app_connector_groups":  self.mapListJSONToList(resp_json.get("appConnectorGroups")),
            "action": resp_json.get("action"),
            "priority": resp_json.get("priority"),
            "operator": resp_json.get("operator"),
            "rule_order": resp_json.get("ruleOrder"),
            "conditions": self.mapConditionsToList(resp_json.get("conditions")),
            "app_server_groups": self.mapListJSONToList(resp_json.get("appServerGroups")),
        }

    @delete_none
    def mapAppToJSON(self, policy_rule):
        if policy_rule is None:
            return {}
        return {
            "defaultRule": policy_rule.get("default_rule"),
            "description": policy_rule.get("description"),
            "policyType": policy_rule.get("policy_type"),
            "customMsg": policy_rule.get("custom_msg"),
            "policySetId": policy_rule.get("policy_set_id"),
            "id": policy_rule.get("id"),
            "reauthDefaultRule": policy_rule.get("reauth_default_rule"),
            "lssDefaultRule": policy_rule.get("lss_default_rule"),
            "reauthDefaultRule": policy_rule.get("bypass_default_rule"),
            "reauthIdleTimeout": policy_rule.get("reauth_idle_timeout"),
            "reauthTimeout": policy_rule.get("reauth_timeout"),
            "actionId": policy_rule.get("action_id"),
            "name": policy_rule.get("name"),
            "action": policy_rule.get("action"),
            "priority": policy_rule.get("priority"),
            "operator": policy_rule.get("operator"),
            "ruleOrder": policy_rule.get("rule_order"),
            "conditions": self.mapConditionsToJSONList(policy_rule.get("conditions")),
            "appServerGroups": self.mapListToJSONObjList(policy_rule.get("app_server_groups")),
            "appConnectorGroups":  self.mapListToJSONObjList(policy_rule.get("app_connector_groups")),
        }

    def customValidate(self, operand, expectedLHS, expectedRHS, getByID):
        if operand.get("lhs", "") == "" or not operand.get("lhs") in expectedLHS:
            return self.lhsWarn(operand.get("objectType"), expectedLHS, operand.get("lhs"), None)
        if operand.get("rhs", "") == "":
            return self.rhsWarn(operand.get("objectType"), expectedRHS, operand.get("rhs"), None)
        resp = getByID(operand.get("rhs"))
        if resp == True:
            return True
        return self.rhsWarn(operand.get("objectType"), expectedRHS, operand.get("rhs"), resp)

    def rhsWarn(self, objType, expected, rhs, err):
        return "[WARN] when operand object type is %s RHS must be an existing %s, value is \"%s\", %s\n" % (objType, expected, rhs, err)

    def lhsWarn(self, objType, expected, lhs, err):
        return "[WARN] when operand object type is %s LHS must be an existing %s value is \"%s\", %s\n" % (objType, expected, lhs, err)

    def reorder(self, rule_id, policy_set_id, order):
        """reorder the Policy rule"""
        response = self.rest.put(
            "/mgmtconfig/v1/admin/customers/%s/policySet/%s/rule/%s/reorder/%s" % (self.customer_id, policy_set_id, rule_id, order))
        status_code = response.status_code
        if status_code > 299:
            return None
        return self.getByID(rule_id, policy_set_id)

    def getAppSegmentByID(self, id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/application/%s" % (self.customer_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return True

    def getSegmentGroupByID(self, id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/segmentGroup/%s" % (self.customer_id, id), fail_safe=True)
        status_code = response.status_code
        if status_code != 200:
            return None
        return True

    def getIDPControllerByID(self, id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/idp/%s" % (self.customer_id, id), fail_safe=True)
        status_code = response.status_code
        if status_code != 200:
            return None
        return True

    def getCloudConnectorGroupByID(self, id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/cloudConnectorGroup/%s" % (self.customer_id, id), fail_safe=True)
        status_code = response.status_code
        if status_code != 200:
            return None
        return True

    def validClientType(self, id):
        if id != "zpn_client_type_zapp" and id != "zpn_client_type_exporter" and id != "zpn_client_type_ip_anchoring" and id != "zpn_client_type_browser_isolation" and id != "zpn_client_type_machine_tunnel" and id != "zpn_client_type_edge_connector":
            return "RHS values must be 'zpn_client_type_zapp' or 'zpn_client_type_exporter' or 'zpn_client_type_ip_anchoring' or 'zpn_client_type_browser_isolation' or 'zpn_client_type_machine_tunnel' or 'zpn_client_type_edge_connector' when object type is CLIENT_TYPE"
        return True

    def getMachineGroupByID(self, id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/machineGroup/%s" % (self.customer_id, id), fail_safe=True)
        status_code = response.status_code
        if status_code != 200:
            return None
        return True

    def getByPostureUDID(self, postureUDID):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v2/admin/customers/%s/posture" % (self.customer_id), data_key_name="list")
        for posture in list:
            if posture.get("postureUdid") == postureUDID:
                return True
        return None

    def getTrustedNetworkByNetID(self, id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/network/%s" % (self.customer_id, id), fail_safe=True)
        status_code = response.status_code
        if status_code != 200:
            return None
        return True

    def getSamlAttribute(self, id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/samlAttribute/%s" % (self.customer_id, id), fail_safe=True)
        status_code = response.status_code
        if status_code != 200:
            return None
        return True

    def getScimAttributeByID(self, id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/idp/scimattribute/%s" % (self.customer_id, id), fail_safe=True)
        status_code = response.status_code
        if status_code != 200:
            return None
        return True

    def getScimGroupByID(self, id):
        response = self.rest.get(
            "/userconfig/v1/customers/%s/scimgroup/%s" % (self.customer_id, id), fail_safe=True)
        status_code = response.status_code
        if status_code != 200:
            return None
        return True

    def validateOperand(self, operand):
        objType = operand.get("objectType")
        if objType == "APP":
            return self.customValidate(operand, ["id"], "application segment ID", lambda id: self.getAppSegmentByID(id))
        elif objType == "APP_GROUP":
            return self.customValidate(operand, ["id"], "Segment Group ID", lambda id: self.getSegmentGroupByID(id))
        elif objType == "IDP":
            return self.customValidate(operand, ["id"], "IDP ID", lambda id: self.getIDPControllerByID(id))
        elif objType == "EDGE_CONNECTOR_GROUP":
            return self.customValidate(operand, ["id"], "cloud connector group ID", lambda id: self.getCloudConnectorGroupByID(id))
        elif objType == "CLIENT_TYPE":
            return self.customValidate(operand, ["id"], "'zpn_client_type_zapp' or 'zpn_client_type_exporter' or 'zpn_client_type_ip_anchoring' or 'zpn_client_type_browser_isolation' or 'zpn_client_type_machine_tunnel' or 'zpn_client_type_edge_connector'", lambda id: self.validClientType(id))
        elif objType == "MACHINE_GRP":
            return self.customValidate(operand, ["id"], "machine group ID", lambda id: self.getMachineGroupByID(id))
        elif objType == "POSTURE":
            if operand.get("lhs") is None or operand.get("lhs") == "":
                return self.lhsWarn(operand.get("objectType"), "valid posture network ID", operand.get("lhs"), None)
            resp = self.getByPostureUDID(operand.get("lhs"))
            if resp != True:
                return self.lhsWarn(operand.get("objectType"), "valid posture network ID", operand.get("lhs"), resp)
            if not operand.get("rhs") in ["true", "false"]:
                return self.rhsWarn(operand.get("objectType"), "\"true\"/\"false\"", operand.get("rhs"), None)
            return True
        elif objType == "TRUSTED_NETWORK":
            if operand.get("lhs") is None or operand.get("lhs") == "":
                return self.lhsWarn(operand.get("objectType"), "valid trusted network ID", operand.get("lhs"), None)
            resp = self.getTrustedNetworkByNetID(operand.get("lhs"))
            if resp != True:
                return self.lhsWarn(operand.get("objectType"), "valid trusted network ID", operand.get("lhs"), resp)
            if operand.get("rhs") != "true":
                return self.rhsWarn(operand.get("objectType"), "\"true\"", operand.get("rhs"), None)
            return True
        elif objType == "SAML":
            if operand.get("lhs") is None or operand.get("lhs") == "":
                return self.lhsWarn(operand.get("objectType"), "valid SAML Attribute ID", operand.get("lhs"), None)
            resp = self.getSamlAttribute(operand.get("lhs"))
            if resp != True:
                return self.lhsWarn(operand.get("objectType"), "valid SAML Attribute ID", operand.get("lhs"), resp)
            if operand.get("rhs") is None or operand.get("rhs") == "":
                return self.rhsWarn(operand.get("objectType"), "SAML Attribute Value", operand.get("rhs"), None)
            return True
        elif objType == "SCIM":
            if operand.get("lhs") is None or operand.get("lhs") == "":
                return self.lhsWarn(operand.get("objectType"), "valid SCIM Attribute ID", operand.get("lhs"), None)
            resp = self.getScimAttributeByID(operand.get("lhs"))
            if resp != True:
                return self.lhsWarn(operand.get("objectType"), "valid SCIM Attribute ID", operand.get("lhs"), resp)
            if operand.get("rhs") is None or operand.get("rhs") == "":
                return self.rhsWarn(operand.get("objectType"), "SCIM Attribute Value", operand.get("rhs"), None)
            return True
        elif objType == "SCIM_GROUP":
            if operand.get("lhs") is None or operand.get("lhs") == "":
                return self.lhsWarn(operand.get("objectType"), "valid IDP Controller ID", operand.get("lhs"), None)
            resp = self.getIDPControllerByID(operand.get("lhs"))
            if resp != True:
                return self.lhsWarn(operand.get("objectType"), "valid IDP Controller ID", operand.get("lhs"), resp)
            if operand.get("rhs") is None or operand.get("rhs") == "":
                return self.rhsWarn(operand.get("objectType"), "SCIM Group ID", operand.get("rhs"), None)
            resp = self.getScimGroupByID(operand.get("rhs"))
            if resp != True:
                return self.rhsWarn(operand.get("objectType"), "SCIM Group ID", operand.get("rhs"), resp)
            return True
        else:
            return "[WARN] invalid operand object type %s\n" % (operand.get("objectType"))

    def validateConditions(self, conditions):
        for condition in conditions:
            for operand in condition.get("operands"):
                check = self.validateOperand(operand)
                if check != True:
                    return check
        return True

    def create(self, policy_rule, policy_set_id):
        """Create new Policy rule"""
        ruleJson = self.mapAppToJSON(policy_rule)
        check = self.validateConditions(
            [] if ruleJson is None else ruleJson.get("conditions"))
        if check != True:
            self.module.fail_json(
                msg="validating policy rule conditions failed: %s" % (check))
        response = self.rest.post(
            "/mgmtconfig/v1/admin/customers/%s/policySet/%s/rule" % (self.customer_id, policy_set_id), data=ruleJson)
        status_code = response.status_code
        if status_code > 299:
            return None
        rule = self.getByID(response.json.get("id"), policy_set_id)
        if policy_rule.get("rule_order") is not None and policy_rule.get("rule_order") != "":
            return self.reorder(rule.get("id"), policy_set_id, policy_rule.get("rule_order"))
        return rule

    def update(self, policy_rule, policy_set_id):
        """update the Policy rule"""
        ruleJson = self.mapAppToJSON(policy_rule)
        check = self.validateConditions(
            [] if ruleJson is None else ruleJson.get("conditions"))
        if check != True:
            self.module.fail_json(
                msg="validating policy rule conditions failed: %s" % (check))
        response = self.rest.put(
            "/mgmtconfig/v1/admin/customers/%s/policySet/%s/rule/%s" % (self.customer_id, policy_set_id, ruleJson.get("id")), data=ruleJson)
        status_code = response.status_code
        if status_code > 299:
            return None
        rule = self.getByID(ruleJson.get("id"), policy_set_id)
        if policy_rule.get("rule_order") is not None and policy_rule.get("rule_order") != "":
            return self.reorder(rule.get("id"), policy_set_id, policy_rule.get("rule_order"))
        return rule

    def delete(self, id, policy_set_id):
        """delete the Policy rule"""
        response = self.rest.delete(
            "/mgmtconfig/v1/admin/customers/%s/policySet/%s/rule/%s" % (self.customer_id, policy_set_id, id))
        return response.status_code
