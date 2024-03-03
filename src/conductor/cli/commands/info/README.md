# conductor-cli-info

## Description

Prints information about the steam library via the CLI

```bash
$ ./bin/conductor-cli info --help
usage: conductor-cli info [-h]

options:
  -h, --help  show this help message and exit
```

Example usage:

```bash
$ ./bin/conductor-cli info         
Shortcuts added to steam:
original VDFDict([('shortcuts', VDFDict([('0', VDFDict([('appid', -400000000), ('AppName', 'game_executable'), ('Exe', '/path/to/game.exe'), ('StartDir', '"/path/to/game"'), ('icon', '/path/to/game/steamgrid/icon.ico'), ('ShortcutPath', ''), ('LaunchOptions', ''), ('IsHidden', 0), ('AllowDesktopConfig', 1), ('AllowOverlay', 1), ('OpenVR', 0), ('Devkit', 0), ('DevkitGameID', ''), ('DevKitOverrideAppID', 0), ('LastPlayTime', 1709296201), ('FlatpakAppId', ''), ('tags', VDFDict([]))]))]))])
{
    "shortcuts": {
        "0": {
            "AllowDesktopConfig": 1,
            "AllowOverlay": 1,
            "AppName": "game_executable",
            "DevKitOverrideAppID": 0,
            "Devkit": 0,
            "DevkitGameID": "",
            "Exe": "/path/to/game.exe",
            "FlatpakAppId": "",
            "IsHidden": 0,
            "LastPlayTime": 1709296201,
            "LaunchOptions": "",
            "OpenVR": 0,
            "ShortcutPath": "",
            "StartDir": "\"/path/to/game\"",
            "appid": 3894967296,
            "icon": "/path/to/game/steamgrid/icon.ico",
            "tags": {}
        }
    }
}
```

## Notes:
- This command will print out the shortcuts that are currently added to steam
- AppId internally in steam is a signed integer, where it may be that positive numbers are official steam games and negative are reserved for non-steam games
(*citation needed here, I have not found any official documentation on this)
- AppIds are exposed to the user as an unsigned integer
- AppId generation is deterministic, and are generated using the app name and the exe path
