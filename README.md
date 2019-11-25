This code is a pared down version of Mr. Mannequin Tools that demonstrates [Mr Mannequins Tools Issue #8](https://github.com/Jim-Kroovy/Mr-Mannequins-Tools/issues/8).

The example code in this project is turning file paths into EnumProperty item identifiers.

The first time we really noticed the problem was when a non-ASCII character appeared in the path. This occurred on Windows 10 when a user had a character like à in their username.

The problem manifested itself by returning a different value in the enum property than was set into it.

## Steps to Reproduce

1. Copy this addon to "$env:APPDATA\Blender Foundation\Blender\2.81\scripts\addons\MrMannequinsTools"
2. Enable the addon
3. In the 3D view, open the Mr Mannequins Tool, select a file, and press print filename.
4. Verify filename correctly printed in console. If console not visible, Window > Toggle System Console.
5. Disable the add on.
6. Rename "$env:APPDATA\Blender Foundation\Blender\2.81\scripts\addons\MrMannequinsTools" to "$env:APPDATA\Blender Foundation\Blender\2.81\scripts\addons\MrMannequinsToolsà"
7. Enable the addon
8. In the 3D view, open the Mr Mannequins Tool, select a file, and press print filename.

### Result

```
Traceback (most recent call last):
  File "C:\Users\doug\AppData\Roaming\Blender Foundation\Blender\2.81\scripts\addons\MrMannequinsTools├á\__init__.py", line 63, in execute
    print("Selected File is {0}".format(MMT.selected_file))
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xfc in position 2: invalid start byte
```
