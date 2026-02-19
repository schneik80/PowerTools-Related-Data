# Configure Hub

[Back to Readme](../README.md)

## Description

**Configure Hub** is a one-time setup command that registers a Fusion Team Hub — along with its templates project and folder — with the Power Tools add-in. Once a hub is configured, the **Create Related Data** command can read templates from that hub automatically.

The command reads the hub, project, and folder directly from the currently open document. No manual ID lookup or JSON editing is required.

---

## When to Run It

- The **first time** you install the add-in on a machine.
- When you **switch to a new hub** that has not been configured yet.
- After a team administrator creates a new templates folder in an additional project.

If the active hub is already configured, the command will notify you and make no changes.

---

## Before You Start

> This setup step is best performed by a Fusion Team administrator, but any team member can run it.

Ensure the following are in place in your Team Hub before running Configure Hub:

1. A **project** accessible to all team members — recommended name: **Templates**.
2. A **folder** inside that project containing your `.f3d` template documents — recommended name: **Related Data** or **Start Parts**.

See [Create Related Data — Setup Step 1](./Related%20Data.md#step-1--create-the-templates-project-and-folder-in-fusion-team) for instructions on creating the templates project and folder.

---

## How to Configure a Hub

1. **Open a template document.** In Fusion, open any `.f3d` file that is already saved inside your templates folder. The document must be saved (not a new unsaved file).

2. **Run Configure Hub.** The command is in the **Design Workspace → Create Panel**.

3. **Review the confirmation dialog.** The dialog shows the detected values read from the open document:

   | Field | Value shown |
   |---|---|
   | Hub | Name of your Autodesk Team Hub |
   | Templates Project | Name of the project containing your templates folder |
   | Templates Folder | Name of the folder containing your template documents |

4. **Click OK** to save the configuration. A confirmation message is shown.

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

Multiple hubs are supported. Each run of Configure Hub appends a new entry for a different hub. Existing entries are never overwritten.

---

## Troubleshooting

| Message | Cause | Resolution |
|---|---|---|
| *Hub Already Added* | The active hub is already in `hub.json` | No action needed — the hub is already configured |
| *No Document Open* | No document is currently open | Open a saved template document first |
| *Document Not Saved* | The open document has not been saved | Save the document and try again |

---

## Access

**Configure Hub** is in the **Design Workspace → Create Panel** and is promoted to the main toolbar by default.

---

[Back to Readme](../README.md)

IMA LLC Copyright
