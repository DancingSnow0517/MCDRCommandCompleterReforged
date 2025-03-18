<div align="center">

# MCDRCommandCompletion Reforged
_✨ Another wonderful implementation of client-side MCDR command completion ✨_

</div>

[Readme zh_CN](/README.md)

> [!WARNING]  
> Requires [FabricMod-MCDRCommandCompletionReforged-Mod](https://github.com/ZhuRuoLing/MCDRCommandCompletionReforged-Mod) to work

## Usage
- Download the latest release of this plugin from [Release](https://github.com/DancingSnow0517/MCDRCommandCompleterReforged/releases) and install it.
- Ensure that the server you join has this mod and the corresponding plugin installed.
- Use `!` in the chat bar to trigger completion.

## Configuration
Configuration file can be found at `config/mccr/config.json`

* ### http_port
  #### `http_port` represents the port used by the HTTP server, this value will be automatically configured to the `server mod` by the command
  - Type: `int`
  - Any integer between `1-65535`
  - Default value: `8080`

## License
This project follows the GNU LGPL V3 license