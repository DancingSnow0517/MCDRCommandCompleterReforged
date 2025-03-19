import asyncio

import uvicorn
# noinspection PyPackageRequirements
from mcdreforged.api.all import *
# noinspection PyPackageRequirements
from mcdreforged.command.command_manager import CommandManager
# noinspection PyPackageRequirements
from mcdreforged.mcdr_server import MCDReforgedServer

from mccr.config import Config

mcdr_server: MCDReforgedServer
command_manager: CommandManager
config: Config

app_server: uvicorn.Server
loop: asyncio.AbstractEventLoop


def on_load(server: PluginServerInterface, old):
    global mcdr_server, command_manager, config, app_server, loop
    # noinspection PyProtectedMember
    mcdr_server = server._mcdr_server
    command_manager = mcdr_server.command_manager
    config = server.load_config_simple(target_class=Config)

    if old is not None:
        while old.loop.is_running():
            pass

    app_server = uvicorn.Server(uvicorn.Config(
        app='mccr.app:app',
        host='127.0.0.1',
        port=config.http_port,
        log_level='critical',
    ))

    start_app_server()

    if server.is_server_running():
        server.execute(f'/configureCompletion localhost:{config.http_port}')


@new_thread("mccr_http_server")
def start_app_server():
    global loop
    loop = asyncio.new_event_loop()
    loop.create_task(app_server.serve())
    loop.run_forever()


def on_unload(server: PluginServerInterface):
    loop.create_task(app_server.shutdown())
    loop.stop()


def on_server_startup(server: PluginServerInterface):
    server.execute(f'/configureCompletion localhost:{config.http_port}')
