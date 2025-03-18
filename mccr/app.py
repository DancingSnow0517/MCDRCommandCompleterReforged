from fastapi import FastAPI
# noinspection PyPackageRequirements
from mcdreforged.command.command_source import PlayerCommandSource
# noinspection PyPackageRequirements
from mcdreforged.info_reactor.info import Info, InfoSource

from mccr import mcdr_server, command_manager

app = FastAPI()


@app.get('/completion')
async def get_completion(player_name: str, command: str):
    if not mcdr_server or not command_manager:
        return []
    command_source = PlayerCommandSource(
        mcdr_server,
        Info(InfoSource.SERVER, ''),
        player_name
    )
    suggestions = command_manager.suggest_command(command, command_source)
    last_element = command.split(' ')[-1].lstrip(' ').rstrip(' ')
    suggest_list = set(suggestion.suggest_input for suggestion in suggestions)
    if len(suggest_list) == 1:
        return suggest_list
    return set(filter(lambda s: s.startswith(last_element), suggest_list))
