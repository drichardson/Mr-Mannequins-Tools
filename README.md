This code is a pared down version of Mr. Mannequin Tools that demonstrates the following issue:

    https://github.com/Jim-Kroovy/Mr-Mannequins-Tools/issues/8 Mr Mannequins Tools

The example code in this project is turning file paths into EnumProperty item identifiers.

The first time we really noticed the problem was when a non-ASCII character appeared in the path. This occurred on Windows 10 when a user had a character like à in their username.

The problem manifested itself by returning a different value in the enum property than was set into it.
