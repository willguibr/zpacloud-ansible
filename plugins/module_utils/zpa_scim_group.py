from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper,delete_none
)


class ScimGroupService:
    def __init__(self, module, customer_id):
        self.module = module
        self.customer_id = customer_id
        self.rest = ZPAClientHelper(module)

    def getByIDOrName(self, id, name, idpName):
        group = None
        if id is not None:
            group = self.getByID(id)
        if group is None and name is not None:
            group = self.getByName(name, idpName)
        return group

    def getByID(self, id):
        response = self.rest.get(
            "/userconfig/v1/customers/%s/scimgroup/%s" % (self.customer_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAllIDPControllersRaw(self):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v2/admin/customers/%s/idp" % (self.customer_id), data_key_name="list")
        return list

    def getIDPByName(self, idpName):
        idps = self.getAllIDPControllersRaw()
        for idp in idps:
            if idp.get("name") == idpName:
                return idp
        return None

    def getAllByIDPName(self, idpName):
        idp = self.getIDPByName(idpName)
        if idp is None:
            return None
        return self.getAll(idp.get("id"))

    def getAll(self, idp_id):
        list = self.rest.get_paginated_data(
            base_url="/userconfig/v1/customers/%s/scimgroup/idpId/%s" % (self.customer_id, idp_id), data_key_name="list")
        groups = []
        for group in list:
            groups.append(self.mapRespJSONToApp(group))
        return groups

    def getByName(self, name, idpName):
        groups = self.getAllByIDPName(idpName)
        for group in groups:
            if group.get("name") == name:
                return group
        return None
    @delete_none
    def mapRespJSONToApp(self, resp_json):
        if resp_json is None:
            return {}
        return {
            "creation_time": resp_json.get("creationTime"),
            "id": resp_json.get("id"),
            "idp_group_id": resp_json.get("idpGroupId"),
            "idp_id": resp_json.get("idpId"),
            "modified_time": resp_json.get("modifiedTime"),
            "name": resp_json.get("name"),
        }
    @delete_none
    def mapAppToJSON(self, group):
        if group is None:
            return {}
        return {
            "creationTime": group.get("creation_time"),
            "id": group.get("id"),
            "idpGroupId": group.get("idp_group_id"),
            "idpId": group.get("idp_id"),
            "modifiedTime": group.get("modified_time"),
            "name": group.get("name"),
        }
