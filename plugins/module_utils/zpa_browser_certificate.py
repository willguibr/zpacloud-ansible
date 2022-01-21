from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper, delete_none
)


class BrowserCertificateService:
    def __init__(self, module, customer_id):
        self.module = module
        self.customer_id = customer_id
        self.rest = ZPAClientHelper(module)

    def getByIDOrName(self, id, name):
        certificate = None
        if id is not None:
            certificate = self.getByID(id)
        if certificate is None and name is not None:
            certificate = self.getByName(name)
        return certificate

    def getByID(self, id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/clientlessCertificate/%s" % (self.customer_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAll(self):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v2/admin/customers/%s/clientlessCertificate/issued" % (self.customer_id), data_key_name="list")
        certificates = []
        for certificate in list:
            certificates.append(self.mapRespJSONToApp(certificate))
        return certificates

    def getByName(self, name):
        certificates = self.getAll()
        for certificate in certificates:
            if certificate.get("name") == name:
                return certificate
        return None

    @delete_none
    def mapRespJSONToApp(self, resp_json):
        if resp_json is None:
            return {}
        return {
            "id": resp_json.get("id"),
            "name": resp_json.get("name"),
        }

    @delete_none
    def mapAppToJSON(self, certificate):
        if certificate is None:
            return {}
        return {
            "id": certificate.get("id"),
            "name": certificate.get("name"),
        }
