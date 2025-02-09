import logging

from regipy.hive_types import SOFTWARE_HIVE_TYPE
from regipy.plugins.plugin import Plugin
from regipy.utils import get_subkey_values_from_list
from regipy.utils import convert_wintime
import datetime

logger = logging.getLogger(__name__)


WIN_VER_PATH = r"\Microsoft\Windows NT\CurrentVersion"
os_list = ("ProductName", "ReleaseID", "CSDVersion", "CurrentVersion", "CurrentBuild", "CurrentBuildNumber", "InstallationType", "EditionID",
           "ProductName", "ProductId", "BuildLab", "BuildLabEx", "CompositionEditionID", "RegisteredOrganization", "RegisteredOwner", "InstallDate")


class WinVersionPlugin(Plugin):
    NAME = 'winver_plugin'
    DESCRIPTION = 'Get relevant OS information'
    COMPATIBLE_HIVE = SOFTWARE_HIVE_TYPE

    def can_run(self):
        # TODO: Choose the relevant condition - to determine if the plugin is relevant for the given hive
        return self.registry_hive.hive_type == SOFTWARE_HIVE_TYPE

    def run(self):
        logger.info("Started winver Plugin...")

        try:
            key = self.registry_hive.get_key(WIN_VER_PATH)
        except RegistryKeyNotFoundException as ex:
            logger.error(f'Could not find {self.NAME} subkey at {WIN_VER_PATH}: {ex}')
            return None

        self.entries = {WIN_VER_PATH: {'last_write': convert_wintime(key.header.last_modified).isoformat()}}

        for val in key.iter_values():
            if val.name in os_list:
                if val.name == "InstallDate":
                    self.entries[WIN_VER_PATH][val.name] = datetime.datetime.utcfromtimestamp(val.value).strftime("%Y-%m-%d %H:%M:%S")
                else:
                    self.entries[WIN_VER_PATH][val.name] = val.value
