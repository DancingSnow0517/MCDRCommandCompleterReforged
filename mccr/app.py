from fastapi import FastAPI

from mccr import get_completion_impl

app = FastAPI()


@app.get('/completion')
async def get_completion(player_name: str, command: str):
    return get_completion_impl(player_name, command)
