# Power Tools for Fusion

Make working as a team, with cloud data, and with assemblies more productive.

## Commands

### [Configure Hub](./docs/Configure%20Hub.md)

To use related data each team member needs to setup the template document folder and hub.

Open a document saved in your templates folder, then run this command to register the hub, project, and folder automatically. Hub configuration is saved to `hub.json` at the add-in root. Multiple hubs are supported.

If you need to remove a hub you can edit the hub json directly.

### [Create Related Data](./docs/Related%20Data.md)

Creates a new related document by copying a template from your configured hub's templates folder and inserting the active document as an external reference. Essential for teams working across multiple disciplines — enables parallel work without permission conflicts or version locking.

- Select from a list of `.f3d` templates stored in your hub.
- New document is auto-named as `<source name> ‹+› <template name>`.
- Templates are cached locally after the first run for faster load times.
