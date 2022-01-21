from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper,
)


class LSSClientTypesService:
    def __init__(self, module, customer_id):
        self.module = module
        self.customer_id = customer_id
        self.rest = ZPAClientHelper(module)

    def getByIDOrName(self, id, name):
        machineGroup = None
        if id is not None:
            machineGroup = self.getByID(id)
        if machineGroup is None and name is not None:
            machineGroup = self.getByName(name)
        return machineGroup

    def getByID(self, id):
        response = self.rest.get(
            "mgmtconfig/v2/admin/lssConfig/clientTypes/%s" % (self.customer_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAll(self):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v2/admin/lssConfig/clientTypes" % ())
        machineGroups = []
        for machineGroup in list:
            machineGroups.append(self.mapRespJSONToApp(machineGroup))
        return machineGroups

    def getByName(self, name):
        machineGroups = self.getAll()
        for machineGroup in machineGroups:
            if machineGroup.get("name") == name:
                return machineGroup
        return None

    def mapRespJSONToApp(self, resp_json):
        if resp_json is None:
            return {}
        return {
            "zpn_client_type_exporter": resp_json.get("ZPNClientTypeExporter"),
            "zpn_client_type_machine_tunnel": resp_json.get("ZPNClientTypeMachineTunnel"),
            "zpn_client_type_ip_anchoring": resp_json.get("ZPNClientTypeIPAnchoring"),
            "zpn_client_type_edge_connector": resp_json.get("ZPNClientTypeEdgeConnector"),
            "zpn_client_type_zapp": resp_json.get("ZPNClientTypeZAPP"),
            "zpn_client_type_slogger": resp_json.get("ZPNClientTypeSlogger"),
        }

    def mapAppToJSON(self, network):
        if network is None:
            return {}
        return {
            "ZPNClientTypeExporter": network.get("zpn_client_type_exporter"),
            "ZPNClientTypeMachineTunnel": network.get("zpn_client_type_machine_tunnel"),
            "ZPNClientTypeIPAnchoring": network.get("zpn_client_type_ip_anchoring"),
            "ZPNClientTypeEdgeConnector": network.get("zpn_client_type_edge_connector"),
            "ZPNClientTypeZAPP": network.get("zpn_client_type_zapp"),
            "ZPNClientTypeSlogger": network.get("zpn_client_type_slogger"),
        }
