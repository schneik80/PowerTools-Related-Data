# PowerTools: Related Data for Autodesk Fusion

Power Tools for Fusion is an Autodesk Fusion add-in that improves team productivity when working with cloud data and assemblies. The **Related Data** add-in lets teams create parallel workflow documents that reference a single source design — without locking, modifying, or duplicating it.

## Prerequisites

- Autodesk Fusion with a **Team Hub** (Commercial, Education, or Start-Up entitlement).
- The add-in installed and loaded in Fusion.
- A templates project and folder set up in your Team Hub. See [Create Related Data — Setup](./docs/Related%20Data.md#setup).

> **Note:** AnyCAD workflows (referencing non-native files such as SolidWorks) require a Team Hub and a Commercial, Education, or Start-Up entitlement. Personal (free/hobby) entitlements do not support AnyCAD.

---

## Commands

### [Configure Hub](./docs/Configure%20Hub.md)

**Configure Hub** is a one-time setup command that registers an Autodesk Fusion Team Hub — along with its templates project and folder — with the add-in. Run this command once per hub, per machine.

Open any `.f3d` document that is already saved inside your templates folder, then run **Configure Hub**. The command detects the hub, project, and folder from the open document automatically. No manual ID lookup or JSON editing is required.

Hub configuration is stored in `hub.json` at the add-in root. Multiple hubs are supported. To remove a hub, edit `hub.json` directly.

**Location:** Quick Access Toolbar → File menu → **PowerTools Settings** flyout

---

### [Create Related Data](./docs/Related%20Data.md)

**Create Related Data** copies a template from your configured hub's templates folder and inserts the active source document as an external reference inside the new document. The result is a *related document* — a separate file linked to the original that can be opened, edited, and managed independently.

Key capabilities:

- Select from a list of `.f3d` templates stored in your hub's templates folder.
- New document is auto-named as `<source name> ‹+› <template name>`.
- Auto-naming can be disabled to provide a custom document name.
- Templates are cached locally after the first run for faster load times.
- The new document is saved in the same folder as the source document.

**Location:** Design Workspace → **Create Panel** (Assembly tab and Solid tab)

---

## Architecture Overview

The add-in is composed of two commands that share a common configuration store.

```mermaid
C4Context
  title System Context — Power Tools Related Data Add-in

  Person(user, "Fusion User", "Runs add-in commands from the Fusion toolbar")

  System_Boundary(addin, "PowerTools Add-in") {
    System(configHub, "Configure Hub", "Registers a Team Hub, project, and folder in hub.json")
    System(relatedData, "Create Related Data", "Creates a new document from a template with an external reference to the source document")
  }

  SystemDb(hubJson, "hub.json", "Local configuration file — stores registered hub IDs, project IDs, and folder IDs")
  SystemDb(cache, "Template Cache", "cache/<hub-id>.json — local cache of available templates per hub")
  SystemExt(fusionTeam, "Autodesk Fusion Team", "Cloud data management — hosts hubs, projects, folders, and .f3d documents")

  Rel(user, configHub, "Runs once per hub")
  Rel(user, relatedData, "Runs to create a related document")
  Rel(configHub, fusionTeam, "Reads hub, project, and folder from active document")
  Rel(configHub, hubJson, "Writes hub entry")
  Rel(relatedData, hubJson, "Reads hub configuration")
  Rel(relatedData, cache, "Reads or writes template list")
  Rel(relatedData, fusionTeam, "Fetches templates (cache miss); saves new document")
```

---

## Getting Started

1. **Create a templates folder** in your Team Hub. See [Create Related Data — Step 1](./docs/Related%20Data.md#step-1--create-the-templates-project-and-folder-in-fusion-team).
2. **Configure the hub.** Open a document saved in your templates folder and run **Configure Hub**. See [Configure Hub](./docs/Configure%20Hub.md).
3. **Create a related document.** Open the source document you want to reference and run **Create Related Data**. See [Create Related Data](./docs/Related%20Data.md).

---

## License

This project is released under the [GNU General Public License v3.0 or later](LICENSE).

Copyright (C) 2022-2026 IMA LLC.

The vendored library at `lib/fusionAddInUtils` is Autodesk sample code and is distributed under its own license terms; see its source headers for details.

---

*Copyright © 2026 IMA LLC. All rights reserved.*
