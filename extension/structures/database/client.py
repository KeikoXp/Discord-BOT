from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import errors as db_errors

from . import models


class DatabaseClient:
    def __init__(self, url: str):
        connection = AsyncIOMotorClient(url)

        database = connection["Marjorie"]

        self.servers = database["Servers"]
        self.players = database["Players"]

    async def get_server(self, id: int) -> models.Server:
        """
        Retorna as informações do servidor, retorna `None` se não
        encontrado.

        Parametros
        ----------
        id : int
            Discord ID do servidor.

        Retorno
        -------
        models.Server
        """
        if type(id) is not int:
            raise TypeError("int expected in `id` parameter")
        
        data = await self.servers.find_one({"_id": str(id)})

        if data:
            return models.Server(data)

    async def get_player(self, id: int) -> models.Player:
        """
        Retorna as informações do jogador, retorna `None` se não
        encontrado.

        Parametros
        ----------
        id : int
            Discord ID do jogador.

        Retorno
        -------
        models.Player
        """
        if type(id) is not int:
            raise TypeError("int expected in `id` parameter")

        data = await self.players.find_one({"_id": str(id)})

        if data:
            return models.Player(data)

    async def new_server(self, server: models.Server) -> None:
        """
        Parametros
        ----------
        server : models.Server

        Raises
        ------
        ValueError
            O servidor já foi registrado.
        """
        if not isinstance(server, models.Server):
            raise TypeError("models.Server expected in `server` parameter")

        server = server.to_dict()
        try:
            return await self.servers.insert_one(server)
        except db_errors.DuplicateKeyError:
            raise ValueError("guild already registred")

    async def new_player(self, player: models.Player) -> None:
        """
        Parametros
        ----------
        player : models.Player

        Raises
        ------
        ValueError
            O jogador já foi registrado.
        """
        if not isinstance(player, models.Player):
            raise TypeError("models.Player expected in `player` parameter")

        player = player.to_dict()
        try:
            return await self.players.insert_one(player)
        except db_errors.DuplicateKeyError:
            raise ValueError("player already registred")
