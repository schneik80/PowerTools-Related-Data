# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2022-2026 IMA LLC

import adsk.core
import os
import os.path
import json
from .lib import fusionAddInUtils as futil

DEBUG = True
ADDIN_NAME = os.path.basename(os.path.dirname(__file__))
COMPANY_NAME = "IMA LLC"

# Root path of the add-in and cache directory.
ADDIN_PATH = os.path.dirname(os.path.realpath(__file__))
CACHE_PATH = os.path.join(ADDIN_PATH, "cache")

# List of allowed hub IDs, populated by loadHub().
COMPANY_HUB = []

# Per-hub config: hub_id -> {"name": str, "project_id": str, "folder_id": str}
COMPANY_HUB_CONFIGS = {}


def loadHub(__file__):
    """Load hub configuration from hub.json and populate COMPANY_HUB / COMPANY_HUB_CONFIGS."""
    global COMPANY_HUB, COMPANY_HUB_CONFIGS

    my_addin_path = os.path.dirname(os.path.realpath(__file__))
    my_hub_path = os.path.join(my_addin_path, "hub.json")

    if not os.path.isfile(my_hub_path):
        # No hub configured yet — commands will surface their own error message.
        COMPANY_HUB = []
        COMPANY_HUB_CONFIGS = {}
        return

    with open(my_hub_path) as json_file:
        hub_data = json.load(json_file)

    hubs = hub_data.get("hubs", [])
    COMPANY_HUB = [entry["id"] for entry in hubs]
    COMPANY_HUB_CONFIGS = {
        entry["id"]: {
            "name": entry.get("name", ""),
            "project_id": entry.get("project_id", ""),
            "project_name": entry.get("project_name", ""),
            "folder_id": entry.get("folder_id", ""),
            "folder_name": entry.get("folder_name", ""),
        }
        for entry in hubs
    }


def reload_hub_config():
    """Reload hub configuration from disk. Call after hub.json is written."""
    loadHub(__file__)


loadHub(__file__)

design_workspace = "FusionSolidEnvironment"
tools_tab_id = "ToolsTab"
my_tab_name = "Power Tools"

my_panel_id = f"PT_{my_tab_name}"
my_panel_name = "Power Tools"
my_panel_after = ""
