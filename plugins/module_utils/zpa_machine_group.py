from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper, delete_none
)


class MachineGroupService:
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
            "/mgmtconfig/v1/admin/customers/%s/machineGroup/%s" % (self.customer_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAll(self):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v1/admin/customers/%s/machineGroup" % (self.customer_id), data_key_name="list")
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
    @delete_none
    def mapRespJSONToApp(self, resp_json):
        if resp_json is None:
            return {}
        return {
            "creation_time": resp_json.get("creationTime"),
            "description": resp_json.get("description"),
            "enabled": resp_json.get("enabled"),
            "id": resp_json.get("id"),
            "modified_by": resp_json.get("modifiedBy"),
            "modified_time": resp_json.get("modifiedTime"),
            "name": resp_json.get("name"),
            # "machines": resp_json.get("machines"), # Machines inner menu is missing
        }
    @delete_none
    def mapAppToJSON(self, network):
        if network is None:
            return {}
        return {
            "creationTime": network.get("creation_time"),
            "description": network.get("description"),
            "enabled": network.get("enabled"),
            "id": network.get("id"),
            "modifiedBy": network.get("modified_by"),
            "modifiedTime": network.get("modified_time"),
            "name": network.get("name"),
            # "machines": network.get("machines"),  # Machines inner menu is missing
        }
