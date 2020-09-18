# Global Imports
import json
from collections import defaultdict

# Metaparser
from genie.metaparser import MetaParser

# =============================================
# Collection for '/mgmt/tm/ltm/message-routing/generic/transport-config' resources
# =============================================


class LtmMessageroutingTransportconfigSchema(MetaParser):

    schema = {}


class LtmMessageroutingTransportconfig(LtmMessageroutingTransportconfigSchema):
    """ To F5 resource for /mgmt/tm/ltm/message-routing/generic/transport-config
    """

    cli_command = "/mgmt/tm/ltm/message-routing/generic/transport-config"

    def rest(self):

        response = self.device.get(self.cli_command)

        response_json = response.json()

        if not response_json:
            return {}

        return response_json
