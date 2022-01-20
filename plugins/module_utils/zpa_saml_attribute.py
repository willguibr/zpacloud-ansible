from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper,delete_none
)


class SamlAttributeService:
    def __init__(self, module, customer_id):
        self.module = module
        self.customer_id = customer_id
        self.rest = ZPAClientHelper(module)

    def getByIDOrName(self, id, name):
        samlAttribute = None
        if id is not None:
            samlAttribute = self.getByID(id)
        if samlAttribute is None and name is not None:
            samlAttribute = self.getByName(name)
        return samlAttribute

    def getByID(self, id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/samlAttribute/%s" % (self.customer_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAll(self):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v2/admin/customers/%s/samlAttribute" % (self.customer_id), data_key_name="list")
        samlAttributes = []
        for samlAttribute in list:
            samlAttributes.append(self.mapRespJSONToApp(samlAttribute))
        return samlAttributes

    def getByName(self, name):
        samlAttributes = self.getAll()
        for samlAttribute in samlAttributes:
            if samlAttribute.get("name") == name:
                return samlAttribute
        return None
    @delete_none
    def mapRespJSONToApp(self, resp_json):
        if resp_json is None:
            return {}
        return {
            "creation_time": resp_json.get("creationTime"),
            "id": resp_json.get("id"),
            "idp_id": resp_json.get("idpId"),
            "idp_name": resp_json.get("idpName"),
            "modified_by": resp_json.get("modifiedBy"),
            "modified_time": resp_json.get("modifiedTime"),
            "name": resp_json.get("name"),
            "saml_name": resp_json.get("samlName"),
            "user_attribute": resp_json.get("userAttribute"),
        }
    @delete_none
    def mapAppToJSON(self, samlAttribute):
        if samlAttribute is None:
            return {}
        return {
            "creationTime": samlAttribute.get("creation_time"),
            "id": samlAttribute.get("id"),
            "idpId": samlAttribute.get("idp_id"),
            "idpName": samlAttribute.get("idp_name"),
            "modifiedBy": samlAttribute.get("modified_by"),
            "modifiedTime": samlAttribute.get("modified_time"),
            "name": samlAttribute.get("name"),
            "samlName": samlAttribute.get("saml_name"),
            "userAttribute": samlAttribute.get("user_attribute"),
        }
