from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper, camelcaseToSnakeCase
)


class LSSLogFormatsService:
    def __init__(self, module):
        self.module = module
        self.rest = ZPAClientHelper(module)

    def getByLogType(self, logType):
        response = self.rest.get(
            "/mgmtconfig/v2/admin/lssConfig/logType/formats?logType=%s" % (logType))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSON(response.json)

    def mapRespJSON(self, resp_json):
        if resp_json is None:
            return {}
        return camelcaseToSnakeCase(resp_json)
