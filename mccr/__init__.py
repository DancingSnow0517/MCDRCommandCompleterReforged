import asyncio
import json
from typing import Any, Awaitable, Coroutine

import uvicorn
# noinspection PyPackageRequirements
from mcdreforged.api.all import *
# noinspection PyPackageRequirements
from mcdreforged.command.command_manager import CommandManager
from mcdreforged.info_reactor.info import InfoSource
# noinspection PyPackageRequirements
from mcdreforged.mcdr_server import MCDReforgedServer

from mccr.config import Config, CompletionMode

__mcdr_server: MCDReforgedServer
command_manager: CommandManager
config: Config

app_server: uvicorn.Server
loop: asyncio.AbstractEventLoop


class MyInfoFilter(InfoFilter):
    def filter_server_info(self, info: Info) -> bool:
        global __mcdr_server, loop
        ct = info.content
        if ct.startswith("ᅀ兀") and ct.endswith("兀ᅀ"):
            ct = ct.removesuffix("兀ᅀ").removeprefix("ᅀ兀")
            query = try_create_query(ct)
            if query is not None:
                player, command, id = query
                result = get_completion_impl(player, command)
                result["id"] = id
                json_result = json.dumps(result)
                PluginServerInterface.get_instance().execute("ᅀ兀" + json_result + "兀ᅀ")
            return False
        return True

def on_load(server: PluginServerInterface, old):
    global __mcdr_server, command_manager, config, app_server, loop
    # noinspection PyProtectedMember
    __mcdr_server = server._mcdr_server
    command_manager = __mcdr_server.command_manager
    config = server.load_config_simple(target_class=Config)
    server.register_info_filter(MyInfoFilter())

    if config.mode == CompletionMode.STDIO:
        if server.is_server_running():
            server.execute("/configureCompletion stdio")
    elif config.mode == CompletionMode.HTTP:
        if server.is_server_running():
            server.execute(f'/configureCompletion http localhost:{config.http_port}')
        if old is not None and hasattr(old, "loop"):
            while old.loop.is_running():
                pass
        app_server = uvicorn.Server(uvicorn.Config(
            app='mccr.app:app',
            host='127.0.0.1',
            port=config.http_port,
            log_level='critical',
        ))
        run_event_loop(app_server.serve())


@new_thread("mccr_event_loop")
def run_event_loop(defer_task: Coroutine | None) -> None:
    global loop
    loop = asyncio.new_event_loop()
    if defer_task is not None:
        loop.create_task(defer_task)
    loop.run_forever()


def try_create_query(a: str) -> tuple[Any, Any, Any] | None:
    try:
        dic = json.loads(a)
        return dic["playerName"], dic["command"], dic["id"]
    except json.decoder.JSONDecodeError:
        return None


def on_unload(server: PluginServerInterface):
    global loop
    if config.mode == CompletionMode.HTTP and loop is not None:
        loop.create_task(app_server.shutdown())
        loop.stop()


def on_server_startup(server: PluginServerInterface):
    if config.mode == CompletionMode.STDIO:
        server.execute("/configureCompletion stdio")
    elif config.mode == CompletionMode.HTTP:
        server.execute(f'/configureCompletion http localhost:{config.http_port}')


def get_completion_impl(player_name: str, command: str):
    if not __mcdr_server or not command_manager:
        return {
            'completion': [],
            'hint': ''
        }

    command_source = PlayerCommandSource(
        __mcdr_server,
        Info(InfoSource.SERVER, ''),
        player_name
    )
    suggestions = command_manager.suggest_command(command, command_source)
    last_element = command.split(' ')[-1].lstrip(' ').rstrip(' ')
    suggest_list = set(suggestion.suggest_input for suggestion in suggestions)
    return {
        'completion': list(filter(lambda s: s.startswith(last_element), suggest_list)),
        'hint': suggestions.complete_hint if suggestions.complete_hint else ''
    }
