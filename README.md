# Power Tools for Fusion

Make working as a team, with cloud data, and with assemblies more productive.

## Commands

### [Configure Hub](./docs/Configure%20Hub.md)

One-time setup per machine and hub. Open a document saved in your templates folder, then run this command to register the hub, project, and folder automatically. Hub configuration is saved to `hub.json` at the add-in root. Multiple hubs are supported.

### [Create Related Data](./docs/Related%20Data.md)

Creates a new related document by copying a template from your configured hub's templates folder and inserting the active document as an external reference. Essential for teams working across multiple disciplines — enables parallel work without permission conflicts or version locking.

- Select from a list of `.f3d` templates stored in your hub.
- New document is auto-named as `<source name> ‹+› <template name>`.
- Templates are cached locally after the first run for faster load times.

### [Document References](./docs/Reference%20Manager.md)

Shows all data relationships attached to the active document, grouped by type, in a single dialog.

- **Parents** — documents this file references.
- **Children** — documents that reference this file.
- **Drawings** — associated `.f2d` drawing files.
- **Related Data** — related documents linked via the `‹+›` naming convention.
