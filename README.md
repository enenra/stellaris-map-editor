# Stellaris Map Editor
This is a small addon for Blender 4.3+ for editing Stellaris preset maps.

## Functionality
* **Import Map Information** from a Stellaris map file into Blender.
  * Import System name, ID, oosition
  * Import Nebula name, position, radius
  * Import Hyperlane from, to
* **Add, Modify & Remove Map Information** within Blender and see your changes.
  * Add System
  * Add Nebula
  * Add Hyperlane
* **Export Map Information** into a new or an existing Stellaris map file.
  * Export System name, ID, position.
  * Export Nebula name, position, radius
  * Export Hyperlane from, to

## How to Use
### Installation
1. Download the addon from GitHub through the [releases](https://github.com/enenra/stellaris-map-editor/releases).
2. Open Blender and install the addon: `Edit > Preferences > Add-ons > Top right dropdown: Install from Disk...`
3. Put your cursor into the 3D View and then hit `N` to open the sidebar. Open the tab named `SME`.
4. Use the provided buttons to add, import & export. When you have a valid system, nebula, hyperlane selected, you will also have the option to change its information in the SME Panel.

### Usage Notes
* **Import** can take up to 20-30min for larger files (it will look like the window locked up). Open your Blender System Console `Window > Toggle System Console` to get realtime output regarding the import progress.
* On **export** you can either make a new file, which will export all the information in the correct per-line format (but it will not be a usable Stellaris map file - you'll need to add all other components to it outside of systems, nebulae, hyperlanes). You can also export to an existing file, at which point the addon will use names and IDs to update existing lines while leaving all other information intact.
* The addon **doesn't support** multiple nebulae having the same name (they will be merged into one entry). Please instead use localization strings to name multiple nebulae the same.
* The addon **provides feedback** through the Blender System Console on issues it finds on import as well as export, such as hyperlanes pointing to IDs that don't exist on import, and hyperlanes that are missing either to or from, as well as duplicate IDs on export.