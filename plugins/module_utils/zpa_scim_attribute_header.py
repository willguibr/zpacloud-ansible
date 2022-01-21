from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper,delete_none
)


class ScimAttributeHeaderService:
    def __init__(self, module, customer_id):
        self.module = module
        self.customer_id = customer_id
        self.rest = ZPAClientHelper(module)

    def getByIDOrName(self, attribute_id, name):
        scimAttribute = None
        if attribute_id is not None:
            scimAttribute = self.getByID(attribute_id)
        if scimAttribute is None and name is not None:
            scimAttribute = self.getByName(name)
        return scimAttribute

    def getByID(self, attribute_id, idpName):
        idp = self.getIDPByName(idpName)
        if idp is None or idp.get("id") is None:
            return None
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/idp/%s/scimattribute/%s" % (self.customer_id, idp.get("id"), attribute_id))
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
        if idp is None or idp.get("id") is None:
            return []
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v1/admin/customers/%s/idp/%s/scimattribute" % (self.customer_id, idp.get("id")), data_key_name="list")
        scimAttributes = []
        for scimAttribute in list:
            scimAttributes.append(self.mapRespJSONToApp(scimAttribute))
        return scimAttributes

    def getByName(self, name, idpName):
        samlAttributes = self.getAllByIDPName(idpName)
        for samlAttribute in samlAttributes:
            if samlAttribute.get("name") == name:
                return samlAttribute
        return None
    @delete_none
    def mapRespJSONToApp(self, resp_json):
        if resp_json is None:
            return {}
        return {
            "canonical_values": resp_json.get("canonicalValues"),
            "case_sensitive": resp_json.get("caseSensitive"),
            "creation_time": resp_json.get("creationTime"),
            "data_type": resp_json.get("dataType"),
            "description": resp_json.get("description"),
            "id": resp_json.get("id"),
            "idp_id": resp_json.get("idpId"),
            "modified_by": resp_json.get("modifiedBy"),
            "modified_time": resp_json.get("modifiedTime"),
            "multivalued": resp_json.get("multivalued"),
            "mutability": resp_json.get("mutability"),
            "name": resp_json.get("name"),
            "required": resp_json.get("required"),
            "returned": resp_json.get("returned"),
            "schema_uri": resp_json.get("schemaURI"),
            "uniqueness": resp_json.get("uniqueness"),
        }
    @delete_none
    def mapAppToJSON(self, scimAttribute):
        if scimAttribute is None:
            return {}
        return {
            "canonicalValues": scimAttribute.get("canonical_values"),
            "caseSensitive": scimAttribute.get("case_sensitive"),
            "creationTime": scimAttribute.get("creation_time"),
            "dataType": scimAttribute.get("data_type"),
            "description": scimAttribute.get("description"),
            "id": scimAttribute.get("id"),
            "idpId": scimAttribute.get("idp_id"),
            "modifiedBy": scimAttribute.get("modified_by"),
            "modifiedTime": scimAttribute.get("modified_time"),
            "multivalued": scimAttribute.get("multivalued"),
            "mutability": scimAttribute.get("mutability"),
            "name": scimAttribute.get("name"),
            "required": scimAttribute.get("required"),
            "returned": scimAttribute.get("returned"),
            "schemaURI": scimAttribute.get("schema_uri"),
            "uniqueness": scimAttribute.get("uniqueness"),
        }
