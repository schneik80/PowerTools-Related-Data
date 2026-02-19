# Create Related Data

[Back to Readme](../README.md)

## Description

**Create Related Data** is a Fusion add-in command in the **Design Workspace → Create Panel** that copies a pre-configured template document from your Team Hub and inserts the active source document as an external reference inside it.

The result is a new *related document* — a separate file that references your source design without locking or modifying it. Multiple team members can work in their own related documents simultaneously, and each document's lifecycle, permissions, and workspace can be managed independently.

When creating the new related document, select from a configurable list of templates stored in your hub. The add-in auto-names the new document using the pattern `<source name> ‹+› <template name>`, making it easy to understand the relationship at a glance. You can also disable auto-naming to provide a custom name.

> **Requirement:** The source document must be saved before this command can be used.

---

## Use Cases

### Manufacture a Native Fusion 3D Design

Create a Manufacturing related document so a CNC programmer can work in parallel without locking or modifying the original design. When you share your design file, manufacturing setups and toolpaths stay private in their own separate document.

```mermaid
%%{
init: {
'theme':'base',
'themeVariables': {
'primaryColor': '#f0f0f0',
'primaryBorderColor': '#454F61',
'lineColor': '#59cff0',
'tertiaryColor': '#e1ecf5',
'fontSize': '14px'
}
}
}%%

graph TD

a(Manufacturing\n Related Document)
b(Fusion 3D Design)

c((User A))
d((User B))

c -..-> b
d -.-> a --"X-Ref"--> b

```

### AnyCAD — Reference an Uploaded Non-Native File

Upload a SolidWorks (or other CAD) file via Fusion Team, then use this add-in to create Manufacturing or Simulation related documents that reference it. When the source file is updated and saved, the related document can update to the new version.

```mermaid
%%{
init: {
'theme':'base',
'themeVariables': {
'primaryColor': '#f0f0f0',
'primaryBorderColor': '#454F61',
'lineColor': '#59cff0',
'tertiaryColor': '#e1ecf5',
'fontSize': '14px'
}
}
}%%

graph TD

A(SolidWorks Part)
B(Manufacturing\n Related Document)
C(Simulation\n Related Document)

i((User A))
j((User B))

B --"X-Ref"--> A
C --"X-Ref"--> A

i -.-> B
j -.-> C

```

Two related documents — one for Manufacturing, one for Simulation — each with a dedicated user working in parallel. This allows different disciplines to work concurrently without permission conflicts.

> **Note:** AnyCAD workflows require a **Team Hub** and a Commercial, Education, or Start-Up entitlement. Personal (free/hobby) entitlements do not include AnyCAD.

### Render Designs with a Consistent Look

Store lighting rigs, exposure settings, HDRI environments, and camera presets inside a Render template document. Every new render document created from this template starts with a consistent, pre-configured look.

```mermaid
%%{
init: {
'theme':'base',
'themeVariables': {
'primaryColor': '#f0f0f0',
'primaryBorderColor': '#454F61',
'lineColor': '#59cff0',
'tertiaryColor': '#e1ecf5',
'fontSize': '14px'
}
}
}%%

graph TD

A(Fusion Design)
B(Render Related\n Document)

B --"X-Ref"--> A

```

---

## Template Documents

Template documents are `.f3d` files stored in a dedicated folder inside a Team Hub project. The add-in lists every file in that folder as a selectable **Type** when you run the command.

### What to put in a template

- **Active workspace** — Fusion preserves the active workspace when saving, so the new document opens directly in the right workspace (Design, Manufacture, Simulation, Render, etc.).
- **Machine definitions, posts, and fixtures** for manufacturing templates.
- **Material and appearance libraries** for assembly templates.
- **Lighting rigs, render settings, and camera presets** for render templates.
- **Document units preference.**

### Example template set

| Template name | Purpose |
|---|---|
| `MFG - Haas.f3d` | Manufacture workspace with Haas machine, post, and fixture pre-loaded |
| `MFG - Plasma.f3d` | Manufacture workspace with plasma cutter setup and toolpaths |
| `ASSY - in.f3d` | Empty assembly in inches |
| `ASSY - mm.f3d` | Empty assembly in millimetres |
| `VIZ.f3d` | Render studio with custom lighting and floor stage elements |

> **Tip:** Always include a generic empty assembly template so users can create a plain related document when no specialist template is needed.

---

## Setup

### Step 1 — Create the Templates project and folder in Fusion Team

> This step is best performed by a Fusion Team administrator.

1. Sign in to [Fusion Team](https://www.autodesk.com/fusion-team).
2. Create a new project — recommended name: **Templates**.
3. Set project permissions so all team members can access it (use the _All Users_ group or equivalent folder-level permissions).
4. Inside the project, create a folder — recommended name: **Related Data** or **Start Parts**.
5. Create or upload `.f3d` documents into that folder — one file per workflow.

### Step 2 — Configure the Hub (once per machine and hub)

The **Configure Hub** command reads the open document's hub, project, and folder automatically. No manual JSON editing is required.

See the [Configure Hub](./Configure%20Hub.md) documentation for the full walkthrough.

In brief:
1. Open any `.f3d` document that is already saved inside your templates folder.
2. Run **Configure Hub** from the **Design Workspace → Create Panel**.
3. Review the detected Hub, Project, and Folder in the confirmation dialog, then click **OK**.

The hub configuration is written to `hub.json` at the add-in root. Multiple hubs can be configured — run **Configure Hub** once for each hub.

### Step 3 — Use the command

1. Open the source document you want to reference (it must be saved).
2. Run **Create Related Data** from the **Design Workspace → Create Panel**.
3. Select a template from the **Type** drop-down.
4. By default the new document is auto-named as `<source name> ‹+› <template name>`. Uncheck **Auto-Name** to enter a custom name.
5. Click **OK**. The new related document is created, saved in the same folder as the source document, and the source is inserted as an external reference.

![Command in Create Panel](assets/000-CDD.png)

![Create Related Data dialog](assets/001-CDD.png)

![Template type drop-down](assets/002-CDD.png)

---

## Template Cache

After the first successful run, the add-in saves a local cache file at `cache/<hub-id>.json` listing all templates found in the configured folder. Subsequent runs load from the cache instead of querying the API, making the dialog open faster.

**To refresh the cache** (e.g. after adding or renaming templates):

Delete the relevant file from the `cache/` folder at the add-in root. The next run will re-query the folder and rebuild the cache automatically.

---

## Access

**Create Related Data** is in the **Design Workspace → Create Panel** and is promoted to the main toolbar by default.

You can also pin it to the **Shortcuts** (S-key menu) for faster access.

---

Thanks to contributions from:

- [TheEppicJR](https://github.com/TheEppicJR)

[Back to Readme](../README.md)

IMA LLC Copyright
