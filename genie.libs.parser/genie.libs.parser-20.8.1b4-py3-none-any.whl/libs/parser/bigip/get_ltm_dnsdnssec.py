# Global Imports
import json
from collections import defaultdict

# Metaparser
from genie.metaparser import MetaParser

# =============================================
# Collection for '/mgmt/tm/ltm/dns/dnssec' resources
# =============================================


class LtmDnsDnssecSchema(MetaParser):

    schema = {}


class LtmDnsDnssec(LtmDnsDnssecSchema):
    """ To F5 resource for /mgmt/tm/ltm/dns/dnssec
    """

    cli_command = "/mgmt/tm/ltm/dns/dnssec"

    def rest(self):

        response = self.device.get(self.cli_command)

        response_json = response.json()

        if not response_json:
            return {}

        return response_json
