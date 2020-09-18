import typing

from asyncio_dgram import connect
from asyncio import wait_for, TimeoutError

from .models import PlayerModel, ServerModel
from .data_operations import DataOperations
from .exceptions import UnableToConnect, DidNotReceive, InvalidServer


__version__ = "1.1.1"
__url__ = "https://aioquery.readthedocs.io/en/latest/"
__description__ = "Asynchronous source A2S."
__author__ = "WardPearce"
__author_email__ = "wardpearce@protonmail.com"
__license__ = "Apache-2.0 License"


class Server:
    _challenge = None

    S2A_INFO_SOURCE = chr(0x49)

    A2S_PLAYERS = b"\xFF\xFF\xFF\xFF\x55"
    A2S_INFO = b"\xFF\xFF\xFF\xFFTSource Engine Query\x00"

    def __init__(self, ip: str, port: int = 27015, timeout: int = 3):
        """Handles interactions with a source server.

        Paramters
        ---------
        ip: str
            Server IP address.
        port: int
            Port of server, defaults to 27015.
        timeout: int
            How long to wait for the server, defaults to 3 seconds.
        """

        self.ip = ip
        self.port = port
        self.timeout = timeout

    async def _send_recv(self, package: bytes) -> bytes:
        """Sends and recives data.

        Paramters
        ---------
        package: bytes
            Package to send

        Returns
        -------
        bytes

        Raises
        ------
        UnableToConnect
            Raised when connection fails
        DidNotReceive
            Raised when didn't receive data within timeout.
        """

        try:
            stream = await connect((self.ip, self.port))
        except Exception:
            raise UnableToConnect()
        else:
            await stream.send(package)

            try:
                data = await wait_for(stream.recv(), self.timeout)
            except TimeoutError:
                raise DidNotReceive()
            else:
                stream.close()
                return data[0]

    async def info(self) -> ServerModel:
        """Returns details around A2S server.

        Returns
        -------
        ServerModel
            Holds data around server.
        """

        data_opts = DataOperations(
            (await self._send_recv(self.A2S_INFO))[4:]
        )

        header = data_opts.byte()

        if chr(header) == self.S2A_INFO_SOURCE:
            result = {
                "protocol": data_opts.byte(),
                "hostname": data_opts.string(),
                "map": data_opts.string(),
                "game_dir": data_opts.string(),
                "game_desc": data_opts.string(),
                "app_id": data_opts.short(),
                "players": data_opts.byte(),
                "max_players": data_opts.byte(),
                "bots": data_opts.byte(),
                "dedicated": chr(data_opts.byte()),
                "os": chr(data_opts.byte()),
                "password": data_opts.byte(),
                "secure": data_opts.byte(),
                "version": data_opts.string()
            }

            if data_opts.byte():
                result["game_port"] = data_opts.short()
                result["steamid"] = data_opts.long_long()
                result["spec_port"] = data_opts.short()
                result["spec_name"] = data_opts.string()
                result["tags"] = data_opts.string()

            return ServerModel(result)
        else:
            raise InvalidServer()

    async def challenge(self) -> bytes:
        """Get challenge number for A2S_PLAYER query.
        """

        data = await self._send_recv(self.A2S_PLAYERS + b"0xFFFFFFFF")
        self._challenge = data[5:]

        return self._challenge

    async def players(self) -> typing.AsyncGenerator[PlayerModel, None]:
        """Yields players on server.

        Yields
        ------
        PlayerModel
            Holds player data.
        """

        if self._challenge is None:
            await self.challenge()

        data_opts = DataOperations(
            (await self._send_recv(self.A2S_PLAYERS + self._challenge))[4:]
        )

        data_opts.byte()
        number = data_opts.byte()

        for index in range(number):
            data_opts.byte()

            player = {
                "id": index + 1,
                "name": data_opts.string(),
                "frags": data_opts.long(),
                "time": data_opts.float()
            }

            yield PlayerModel(player)
