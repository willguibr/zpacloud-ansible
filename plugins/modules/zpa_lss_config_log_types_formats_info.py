#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from random import choice
from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_lss_log_formats import LSSLogFormatsService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_lss_log_formats_info
short_description: Retrieves LSS Log formats Information.
description:
  - This module will allow the retrieval of LSS (Log Streaming Services) Log formats information from the ZPA Cloud.
author: William Guilherme (@willguibr)
version_added: "1.0.0"
requirements:
  - supported starting from zpa_api >= 2.0
options:
  log_type:
    description:
      - Log type
    required: true
    coices: ["zpn_trans_log", "zpn_auth_log", "zpn_ast_auth_log", "zpn_http_trans_log", "zpn_audit_log", "zpn_ast_comprehensive_stats"]
    type: str
"""

EXAMPLES = """
    - name: Gather LSS Log types formats
      willguibr.zpacloud.zpa_lss_config_log_types_formats_info:
        log_type: zpn_trans_log
      register: log_types_formats
    - name: log_types_formats
      debug:
        msg: "{{ log_types_formats }}"
"""

RETURN = """
data:
    description: LSS Log formats
    returned: success
    elements: dict
    type: list
    sample: [
      {
            "csv": "%s{LogTimestamp:time} User Activity zpa-lss: ,%s{Customer},%s{SessionID},%s{ConnectionID},%s{InternalReason},%s{ConnectionStatus},%d{IPProtocol},%d{DoubleEncryption},%s{Username},%d{ServicePort},%s{ClientPublicIP},%s{ClientPrivateIP},%f{ClientLatitude},%f{ClientLongitude},%s{ClientCountryCode},%s{ClientZEN},%s{Policy},%s{Connector},%s{ConnectorZEN},%s{ConnectorIP},%d{ConnectorPort},%s{Host},%s{Application},%s{AppGroup},%s{Server},%s{ServerIP},%d{ServerPort},%d{PolicyProcessingTime},%d{ServerSetupTime},%s{TimestampConnectionStart:iso8601},%s{TimestampConnectionEnd:iso8601},%s{TimestampCATx:iso8601},%s{TimestampCARx:iso8601},%s{TimestampAppLearnStart:iso8601},%s{TimestampZENFirstRxClient:iso8601},%s{TimestampZENFirstTxClient:iso8601},%s{TimestampZENLastRxClient:iso8601},%s{TimestampZENLastTxClient:iso8601},%s{TimestampConnectorZENSetupComplete:iso8601},%s{TimestampZENFirstRxConnector:iso8601},%s{TimestampZENFirstTxConnector:iso8601},%s{TimestampZENLastRxConnector:iso8601},%s{TimestampZENLastTxConnector:iso8601},%d{ZENTotalBytesRxClient},%d{ZENBytesRxClient},%d{ZENTotalBytesTxClient},%d{ZENBytesTxClient},%d{ZENTotalBytesRxConnector},%d{ZENBytesRxConnector},%d{ZENTotalBytesTxConnector},%d{ZENBytesTxConnector},%s{Idp},%s{c2c}\\n",
            "json": "{\"LogTimestamp\": %j{LogTimestamp:time},\"Customer\": %j{Customer},\"SessionID\": %j{SessionID},\"ConnectionID\": %j{ConnectionID},\"InternalReason\": %j{InternalReason},\"ConnectionStatus\": %j{ConnectionStatus},\"IPProtocol\": %d{IPProtocol},\"DoubleEncryption\": %d{DoubleEncryption},\"Username\": %j{Username},\"ServicePort\": %d{ServicePort},\"ClientPublicIP\": %j{ClientPublicIP},\"ClientPrivateIP\": %j{ClientPrivateIP},\"ClientLatitude\": %f{ClientLatitude},\"ClientLongitude\": %f{ClientLongitude},\"ClientCountryCode\": %j{ClientCountryCode},\"ClientZEN\": %j{ClientZEN},\"Policy\": %j{Policy},\"Connector\": %j{Connector},\"ConnectorZEN\": %j{ConnectorZEN},\"ConnectorIP\": %j{ConnectorIP},\"ConnectorPort\": %d{ConnectorPort},\"Host\": %j{Host},\"Application\": %j{Application},\"AppGroup\": %j{AppGroup},\"Server\": %j{Server},\"ServerIP\": %j{ServerIP},\"ServerPort\": %d{ServerPort},\"PolicyProcessingTime\": %d{PolicyProcessingTime},\"ServerSetupTime\": %d{ServerSetupTime},\"TimestampConnectionStart\": %j{TimestampConnectionStart:iso8601},\"TimestampConnectionEnd\": %j{TimestampConnectionEnd:iso8601},\"TimestampCATx\": %j{TimestampCATx:iso8601},\"TimestampCARx\": %j{TimestampCARx:iso8601},\"TimestampAppLearnStart\": %j{TimestampAppLearnStart:iso8601},\"TimestampZENFirstRxClient\": %j{TimestampZENFirstRxClient:iso8601},\"TimestampZENFirstTxClient\": %j{TimestampZENFirstTxClient:iso8601},\"TimestampZENLastRxClient\": %j{TimestampZENLastRxClient:iso8601},\"TimestampZENLastTxClient\": %j{TimestampZENLastTxClient:iso8601},\"TimestampConnectorZENSetupComplete\": %j{TimestampConnectorZENSetupComplete:iso8601},\"TimestampZENFirstRxConnector\": %j{TimestampZENFirstRxConnector:iso8601},\"TimestampZENFirstTxConnector\": %j{TimestampZENFirstTxConnector:iso8601},\"TimestampZENLastRxConnector\": %j{TimestampZENLastRxConnector:iso8601},\"TimestampZENLastTxConnector\": %j{TimestampZENLastTxConnector:iso8601},\"ZENTotalBytesRxClient\": %d{ZENTotalBytesRxClient},\"ZENBytesRxClient\": %d{ZENBytesRxClient},\"ZENTotalBytesTxClient\": %d{ZENTotalBytesTxClient},\"ZENBytesTxClient\": %d{ZENBytesTxClient},\"ZENTotalBytesRxConnector\": %d{ZENTotalBytesRxConnector},\"ZENBytesRxConnector\": %d{ZENBytesRxConnector},\"ZENTotalBytesTxConnector\": %d{ZENTotalBytesTxConnector},\"ZENBytesTxConnector\": %d{ZENBytesTxConnector},\"Idp\": %j{Idp},\"ClientToClient\": %j{c2c}}\\n",
            "tsv": "%s{LogTimestamp:time} User Activity zpa-lss: \\t%s{Customer}\\t%s{SessionID}\\t%s{ConnectionID}\\t%s{InternalReason}\\t%s{ConnectionStatus}\\t%d{IPProtocol}\\t%d{DoubleEncryption}\\t%s{Username}\\t%d{ServicePort}\\t%s{ClientPublicIP}\\t%s{ClientPrivateIP}\\t%f{ClientLatitude}\\t%f{ClientLongitude}\\t%s{ClientCountryCode}\\t%s{ClientZEN}\\t%s{Policy}\\t%s{Connector}\\t%s{ConnectorZEN}\\t%s{ConnectorIP}\\t%d{ConnectorPort}\\t%s{Host}\\t%s{Application}\\t%s{AppGroup}\\t%s{Server}\\t%s{ServerIP}\\t%d{ServerPort}\\t%d{PolicyProcessingTime}\\t%d{ServerSetupTime}\\t%s{TimestampConnectionStart:iso8601}\\t%s{TimestampConnectionEnd:iso8601}\\t%s{TimestampCATx:iso8601}\\t%s{TimestampCARx:iso8601}\\t%s{TimestampAppLearnStart:iso8601}\\t%s{TimestampZENFirstRxClient:iso8601}\\t%s{TimestampZENFirstTxClient:iso8601}\\t%s{TimestampZENLastRxClient:iso8601}\\t%s{TimestampZENLastTxClient:iso8601}\\t%s{TimestampConnectorZENSetupComplete:iso8601}\\t%s{TimestampZENFirstRxConnector:iso8601}\\t%s{TimestampZENFirstTxConnector:iso8601}\\t%s{TimestampZENLastRxConnector:iso8601}\\t%s{TimestampZENLastTxConnector:iso8601}\\t%d{ZENTotalBytesRxClient}\\t%d{ZENBytesRxClient}\\t%d{ZENTotalBytesTxClient}\\t%d{ZENBytesTxClient}\\t%d{ZENTotalBytesRxConnector}\\t%d{ZENBytesRxConnector}\\t%d{ZENTotalBytesTxConnector}\\t%d{ZENBytesTxConnector}\\t%s{Idp}\\t%s{c2c}\\n"
      }
    ]
"""


def core(module):
    service = LSSLogFormatsService(module)
    log_type = module.params.get("log_type", None)
    lss_log_formats = service.getByLogType(log_type)
    module.exit_json(changed=False, data=lss_log_formats)


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    argument_spec.update(
        log_type=dict(type="str", required=True, choices=[
                      "zpn_trans_log", "zpn_auth_log", "zpn_ast_auth_log", "zpn_http_trans_log", "zpn_audit_log", "zpn_ast_comprehensive_stats"]),
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
