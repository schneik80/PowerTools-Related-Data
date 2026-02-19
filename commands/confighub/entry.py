import adsk.core
import os, os.path
import json
from ...lib import fusionAddInUtils as futil
from ... import config

# Module-level vars used to pass data from command_created to command_execute.
_pending_hub_id = ""
_pending_hub_name = ""
_pending_project_id = ""
_pending_project_name = ""
_pending_folder_id = ""
_pending_folder_name = ""

app = adsk.core.Application.get()
ui = app.userInterface

# Command identity information.
CMD_ID = f"{config.COMPANY_NAME}_{config.ADDIN_NAME}_configHub"
CMD_NAME = "Configure Hub"
CMD_Description = "Configure the Team Hub for Power Tools"

# QAT flyout (shared across PowerTools add-ins — create only if absent).
PT_SETTINGS_ID = "PTSettings"
PT_SETTINGS_NAME = "PowerTools Settings"

# Resource location for command icons, here we assume a sub folder in this directory named "resources".
ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "")

# Path to hub.json at the add-in root (two levels up from this file's directory).
ADDIN_PATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
HUB_JSON_PATH = os.path.join(ADDIN_PATH, "hub.json")

# Local list of event handlers used to maintain a reference so
# they are not released and garbage collected.
local_handlers = []


# Executed when add-in is run.
def start():
    # Create a command Definition.
    cmd_def = ui.commandDefinitions.addButtonDefinition(
        CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER
    )

    # Define an event handler for the command created event. It will be called when the button is clicked.
    futil.add_handler(cmd_def.commandCreated, command_created)

    # ******** Add a button into the UI so the user can run the command. ********
    # Get the QAT toolbar.
    qat = ui.toolbars.itemById("QAT")

    # Get the drop-down that contains the file related commands.
    file_dropdown = adsk.core.DropDownControl.cast(qat.controls.itemById("FileSubMenuCommand"))

    # Get or create the shared PowerTools Settings flyout.
    # Other PowerTools add-ins may have already added this flyout.
    pt_settings_control = file_dropdown.controls.itemById(PT_SETTINGS_ID)
    if not pt_settings_control:
        pt_settings = file_dropdown.controls.addDropDown(
            PT_SETTINGS_NAME, "", PT_SETTINGS_ID
        )
    else:
        pt_settings = adsk.core.DropDownControl.cast(pt_settings_control)

    # Add the command into the flyout.
    pt_settings.controls.addCommand(cmd_def)


# Executed when add-in is stopped.
def stop():
    # Get the various UI elements for this command
    qat = ui.toolbars.itemById("QAT")
    file_dropdown = adsk.core.DropDownControl.cast(qat.controls.itemById("FileSubMenuCommand"))
    pt_settings = adsk.core.DropDownControl.cast(file_dropdown.controls.itemById(PT_SETTINGS_ID))

    if pt_settings:
        command_control = pt_settings.controls.itemById(CMD_ID)
        if command_control:
            command_control.deleteMe()

        # Only remove the flyout if no other add-in's commands remain.
        if pt_settings.controls.count == 0:
            pt_settings.deleteMe()

    command_definition = ui.commandDefinitions.itemById(CMD_ID)
    if command_definition:
        command_definition.deleteMe()


def _load_hubs():
    """Return the hubs list from hub.json, or an empty list if the file does not exist."""
    if not os.path.isfile(HUB_JSON_PATH):
        return []
    with open(HUB_JSON_PATH) as f:
        data = json.load(f)
    return data.get("hubs", [])


def _hub_is_listed(hub_id, hubs):
    """Return True if hub_id is already present in the hubs list."""
    return any(entry.get("id") == hub_id for entry in hubs)


def _find_project_for_folder(hub, folder):
    """Walk *folder* up to the root DataFolder then find which DataProject owns it."""
    root = folder
    try:
        while root.parentFolder is not None:
            root = root.parentFolder
    except Exception:
        pass

    for project in hub.dataProjects:
        try:
            if project.rootFolder.id == root.id:
                return project
        except Exception:
            continue
    return None


# Function that is called when a user clicks the corresponding button in the UI.
# This defines the contents of the command dialog and connects to the command related events.
def command_created(args: adsk.core.CommandCreatedEventArgs):
    futil.log(f"{CMD_NAME} Command Created Event")

    global _pending_hub_id, _pending_hub_name, _pending_project_id, _pending_project_name, _pending_folder_id, _pending_folder_name

    inputs = args.command.commandInputs
    active_hub = app.data.activeHub

    # Load the current hub list (may be empty if hub.json doesn't exist yet).
    hubs = _load_hubs()

    # If the active hub is already in the list there is nothing to do.
    if _hub_is_listed(active_hub.id, hubs):
        ui.messageBox(
            f'"{active_hub.name}" is already configured.\nNo changes were made.',
            "Hub Already Added",
            0,
            2,
        )
        return

    # A document must be open and saved so we can read its parent folder/project.
    if app.activeDocument is None:
        ui.messageBox(
            "No document is open.\nPlease open a saved document that lives in your "
            "templates folder before configuring the hub.",
            "No Document Open",
            0,
            3,
        )
        return

    if app.activeDocument.isSaved is False:
        ui.messageBox(
            "The active document has not been saved.\nPlease save the document and try again.",
            "Document Not Saved",
            0,
            3,
        )
        return

    # Gather location info from the active document.
    doc_folder = app.activeDocument.dataFile.parentFolder
    folder_id = doc_folder.id
    folder_name = doc_folder.name

    project = _find_project_for_folder(active_hub, doc_folder)
    project_id = project.id if project else ""
    project_name = project.name if project else "(unknown)"

    hub_name = active_hub.name

    futil.log(
        f"{CMD_NAME} Hub: {hub_name} | Project: {project_name} ({project_id}) "
        f"| Folder: {folder_name} ({folder_id})"
    )

    # Stash values so command_execute can write them without re-querying the API.
    _pending_hub_id = active_hub.id
    _pending_hub_name = hub_name
    _pending_project_id = project_id
    _pending_project_name = project_name
    _pending_folder_id = folder_id
    _pending_folder_name = folder_name

    # Build read-only confirmation dialog.
    hub_name_input = inputs.addStringValueInput("hubNameInput", "Hub", hub_name)
    hub_name_input.isEnabled = False

    project_input = inputs.addStringValueInput(
        "projectInput", "Templates Project", project_name
    )
    project_input.isEnabled = False

    folder_input = inputs.addStringValueInput(
        "parentFolderInput", "Templates Folder", folder_name
    )
    folder_input.isEnabled = False

    # Connect to the events.
    futil.add_handler(
        args.command.execute, command_execute, local_handlers=local_handlers
    )
    futil.add_handler(
        args.command.destroy, command_destroy, local_handlers=local_handlers
    )


# This event handler is called when the user clicks the OK button in the command dialog.
def command_execute(args: adsk.core.CommandEventArgs):
    futil.log(f"{CMD_NAME} Command Execute Event")

    global _pending_hub_id, _pending_hub_name, _pending_project_id, _pending_project_name, _pending_folder_id, _pending_folder_name

    # Load the existing list (or start fresh) and append the new hub entry with
    # its templates project/folder so relateddata can look up the right files.
    hubs = _load_hubs()
    hubs.append(
        {
            "id": _pending_hub_id,
            "name": _pending_hub_name,
            "project_id": _pending_project_id,
            "project_name": _pending_project_name,
            "folder_id": _pending_folder_id,
            "folder_name": _pending_folder_name,
        }
    )

    with open(HUB_JSON_PATH, "w") as f:
        json.dump({"hubs": hubs}, f, indent=2)

    futil.log(f"{CMD_NAME} hub.json updated: {hubs}")

    # Reload in-memory config so all commands immediately see the new hub.
    config.reload_hub_config()

    ui.messageBox(
        f"Hub added successfully."
        f"\nHub: {_pending_hub_name}"
        f"\nProject: {_pending_project_name}"
        f"\nFolder: {_pending_folder_name}",
        "Hub Configured",
        0,
        2,
    )


# This event handler is called when the command terminates.
def command_destroy(args: adsk.core.CommandEventArgs):
    futil.log(f"{CMD_NAME} Command Destroy Event")

    global local_handlers
    local_handlers = []
