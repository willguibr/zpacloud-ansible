from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper, delete_none
)


class PostureProfileService:
    def __init__(self, module, customer_id):
        self.module = module
        self.customer_id = customer_id
        self.rest = ZPAClientHelper(module)

    def getByIDOrName(self, id, name):
        posture = None
        if id is not None:
            posture = self.getByID(id)
        if posture is None and name is not None:
            posture = self.getByName(name)
        return posture

    def getByID(self, id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/posture/%s" % (self.customer_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAll(self):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v2/admin/customers/%s/posture" % (self.customer_id), data_key_name="list")
        postures = []
        for posture in list:
            postures.append(self.mapRespJSONToApp(posture))
        return postures

    def getByName(self, name):
        postures = self.getAll()
        for posture in postures:
            if posture.get("name") == name:
                return posture
        return None
    @delete_none
    def mapRespJSONToApp(self, resp_json):
        if resp_json is None:
            return {}
        return {
            "creation_time": resp_json.get("creationTime"),
            "domain": resp_json.get("domain"),
            "id": resp_json.get("id"),
            "master_customer_id": resp_json.get("masterCustomerId"),
            "modified_by": resp_json.get("modifiedBy"),
            "modified_time": resp_json.get("modifiedTime"),
            "name": resp_json.get("name"),
            "posture_udid": resp_json.get("postureUdid"),
            "zscaler_cloud": resp_json.get("zscalerCloud"),
            "zscaler_customer_id": resp_json.get("zscalerCustomerId"),
        }
    @delete_none
    def mapAppToJSON(self, posture):
        if posture is None:
            return {}
        return {
            "creationTime": posture.get("creation_time"),
            "domain": posture.get("domain"),
            "id": posture.get("id"),
            "masterCustomerId": posture.get("master_customer_id"),
            "modifiedBy": posture.get("modified_by"),
            "modifiedTime": posture.get("modified_time"),
            "name": posture.get("name"),
            "postureUdid": posture.get("posture_udid"),
            "zscalerCloud": posture.get("zscaler_cloud"),
            "zscalerCustomerId": posture.get("zscaler_customer_id"),
        }
