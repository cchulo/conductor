# conductor-cli-add_shortcut

## Description

Adds a non-steam game to the steam library via the CLI


```bash
$ ./bin/conductor-cli add_shortcut --help
usage: conductor-cli add_shortcut [-h] --name <name> --path <path/to/executable> [--compat-tool <compat_tool>] [--hero <path/to/hero/image>] [--logo <path/to/logo/image>] [--tenfoot <path/to/tenfoot/image>] [--boxart <path/to/boxart/image>] [--icon <path/to/icon/image>] [--launch-options <launch options>]

options:
  -h, --help            show this help message and exit
  --app-name <name>     (Required) The name of the shortcut
  --exe-path <path/to/executable>
                        (Required) The full path to the executable
  --compat-tool <compat_tool>
                        The name of the compatability tool to use
  --hero <path/to/hero/image>
                        The path to the hero image
  --logo <path/to/logo/image>
                        The path to the logo image
  --tenfoot <path/to/tenfoot/image>
                        The path to the tenfoot image
  --boxart <path/to/boxart/image>
                        The path to the boxart image
  --icon <path/to/icon/image>
                        The path to the icon image
  --launch-options <launch options>
                        The launch options for the shortcut
  --dry-run             Performs a dry run
```

Example usage:

```bash
$ ./bin/conductor-cli add_shortcut \
  --name "My Game" \
  --path "/path/to/my/game/executable" \
  --launch-options "-fullscreen -resolution 1920x1080"

$ ./bin/conductor-cli add_shortcut \
  --name "My Game" \
  --path "/path/to/my/game/executable" \
  --launch-options "-fullscreen -resolution 1920x1080" \
  --icon "/path/to/icon/image.png" \
  --boxart "/path/to/boxart/image.png" \
  --tenfoot "/path/to/tenfoot/image.png" \
  --logo "/path/to/logo/image.png" \
  --hero "/path/to/hero/image.png" \
  --compat-tool "GE-Proton8-32"
```

## Notes:
- You can run this while steam is open, however you will need to restart steam upon completion for the changes to take effect
- Compatibility tools are the same as those found in the steam client, and they are assumed to be installed prior to running this command,
if it happens to work anyway, it will be considered undefined behavior as I do not have a complete understanding of how steam is coded
- The images are assumed to be in a format that steam can understand, and they are assumed to be in a location that steam can access
- The launch options are passed directly to the executable, so they should be formatted as such
- It is entirely possible that there can be collisions with steam shortcuts. The algorithm used to generate random AppId was taken directly from SteamTinkerLaunch.
Added a mitigation for this to prevent duplicate AppIds from being generated, but it is not guaranteed to be foolproof.
Will need to fall back to a different seeding method if this becomes a problem.
