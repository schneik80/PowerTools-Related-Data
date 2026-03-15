# Configure Hub

[Back to Readme](../README.md)

## Overview

**Configure Hub** is a one-time setup command that registers an Autodesk Fusion Team Hub — along with its templates project and folder — with the Power Tools add-in. After a hub is configured, the **Create Related Data** command can read templates from that hub automatically.

The command reads the hub, project, and folder directly from the currently open document. No manual ID lookup or JSON editing is required.

---

## When to run Configure Hub

Run **Configure Hub** in the following situations:

- The **first time** you install the add-in on a machine.
- When you **connect to a new hub** that has not been configured on that machine yet.
- After a team administrator creates a new templates folder in a different hub.

If the active hub is already configured, the command notifies you and makes no changes.

---

## Prerequisites

Before running **Configure Hub**, ensure the following are in place in your Team Hub:

1. A **project** accessible to all team members — recommended name: **Templates**.
2. A **folder** inside that project containing your `.f3d` template documents — recommended name: **Related Data** or **Start Parts**.
3. A saved `.f3d` document inside that folder to open in Fusion.

See [Create Related Data — Step 1](./Related%20Data.md#step-1--create-the-templates-project-and-folder-in-fusion-team) for instructions on creating the templates project and folder.

> This setup step is best performed by a Fusion Team administrator, but any team member can run it.

---

## How to configure a hub

1. **Open a template document.** In Fusion, open any `.f3d` file that is already saved inside your templates folder. The document must be saved — unsaved documents cannot be used.

2. **Run Configure Hub.** Select **Configure Hub** from the **Quick Access Toolbar → File menu → PowerTools Settings** flyout.

3. **Review the confirmation dialog.** The dialog displays the values detected from the open document:

   | Field | Description |
   |---|---|
   | Hub | Name of your Autodesk Team Hub |
   | Templates Project | Name of the project that contains your templates folder |
   | Templates Folder | Name of the folder that contains your template documents |

4. **Click OK** to save the configuration. A confirmation message confirms the hub was added successfully.

The hub entry is written to `hub.json` at the add-in root in the following format:

```json
{
  "hubs": [
    {
      "id": "a.XXXXXXXXXXXXXXXX",
      "name": "Your Hub Name",
      "project_id": "a.XXXXXXXXXXXXXXXX",
      "project_name": "Templates",
      "folder_id": "urn:adsk.wipprod:fs.folder:co.XXXXXXXXXXXXXXXX",
      "folder_name": "Related Data"
    }
  ]
}
```

Multiple hubs are supported. Each run of **Configure Hub** appends a new entry for a different hub. Existing entries are never overwritten.

To remove a hub, open `hub.json` and delete the corresponding entry from the `hubs` array.

---

## Troubleshooting

| Message | Cause | Resolution |
|---|---|---|
| *Hub Already Added* | The active hub is already present in `hub.json` | No action is needed — the hub is already configured |
| *No Document Open* | No document is currently open in Fusion | Open a saved `.f3d` document from your templates folder and try again |
| *Document Not Saved* | The open document has not been saved to the Team Hub | Save the document to your templates folder and try again |

---

## Architecture

### How the command works

When you run **Configure Hub**, the add-in follows this sequence:

1. Checks whether the active hub ID is already present in `hub.json`. If it is, the command exits without making changes.
2. Verifies that a document is open and saved.
3. Reads the active document's parent folder from the Fusion API, then walks up the folder hierarchy to locate the root project folder.
4. Matches the root folder against the hub's data projects to identify the project name and ID.
5. Displays a read-only confirmation dialog showing the detected hub, project, and folder values.
6. On confirmation (OK), appends the new hub entry to `hub.json` and reloads the in-memory configuration so all commands immediately see the new hub.

### System context

```mermaid
C4Context
  title System Context — Configure Hub

  Person(user, "Fusion User", "Runs Configure Hub once per hub, per machine")

  System_Boundary(addin, "PowerTools Add-in") {
    System(configHub, "Configure Hub Command", "Reads the open document's location and writes hub configuration to disk")
  }

  SystemExt(fusionTeam, "Autodesk Fusion Team", "Hosts the hub, projects, folders, and template .f3d files")
  SystemDb(hubJson, "hub.json", "Local file at the add-in root — stores registered hub IDs, project IDs, and folder IDs")

  Rel(user, configHub, "Opens a template document, then runs Configure Hub")
  Rel(configHub, fusionTeam, "Reads the active document hub, project, and folder via Fusion API")
  Rel(configHub, hubJson, "Appends the new hub entry on confirmation")
```

### Container detail

```mermaid
C4Container
  title Container Diagram — Configure Hub

  Person(user, "Fusion User")

  Container_Boundary(addin, "PowerTools Add-in") {
    Container(cmdCreated, "command_created handler", "Python / Fusion API", "Validates preconditions; detects hub, project, and folder from the active document; builds the read-only confirmation dialog")
    Container(cmdExecute, "command_execute handler", "Python / json", "Appends the hub entry to hub.json; calls config.reload_hub_config()")
    Container(configModule, "config.py", "Python", "Loads and exposes COMPANY_HUB and COMPANY_HUB_CONFIGS in memory from hub.json")
  }

  SystemDb(hubJson, "hub.json", "Local JSON configuration file at the add-in root")
  SystemExt(fusionApi, "Fusion API (adsk.core)", "Provides activeHub, activeDocument, dataFile, parentFolder, and dataProjects")

  Rel(user, cmdCreated, "Clicks Configure Hub")
  Rel(cmdCreated, fusionApi, "Reads active hub, document folder, and project IDs")
  Rel(cmdCreated, cmdExecute, "Passes pending hub data when the user clicks OK")
  Rel(cmdExecute, hubJson, "Writes the updated hubs array")
  Rel(cmdExecute, configModule, "Calls reload_hub_config()")
  Rel(configModule, hubJson, "Reads hub entries on load or reload")
```

---

## Access

**Configure Hub** is in the **Quick Access Toolbar → File menu → PowerTools Settings** flyout.

---

[Back to Readme](../README.md)

Copyright IMA LLC. All rights reserved.
