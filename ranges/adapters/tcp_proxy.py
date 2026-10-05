"""Minimal TCP gateway from published ports to a target on an internal network."""
from __future__ import annotations

import asyncio
import os


TARGET = os.environ["TARGET_HOST"]
PORTS = [int(value) for value in os.environ["TARGET_PORTS"].split(",") if value]


async def _copy(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    try:
        while data := await reader.read(65536):
            writer.write(data)
            await writer.drain()
    except (ConnectionError, asyncio.CancelledError):
        pass
    finally:
        writer.close()


async def _forward(
    client_reader: asyncio.StreamReader, client_writer: asyncio.StreamWriter, port: int
) -> None:
    try:
        target_reader, target_writer = await asyncio.open_connection(TARGET, port)
    except OSError:
        client_writer.close()
        await client_writer.wait_closed()
        return
    await asyncio.gather(
        _copy(client_reader, target_writer),
        _copy(target_reader, client_writer),
    )


async def main() -> None:
    servers = []
    for port in PORTS:
        servers.append(
            await asyncio.start_server(
                lambda reader, writer, selected=port: _forward(
                    reader, writer, selected
                ),
                "0.0.0.0",
                port,
            )
        )
    async with asyncio.TaskGroup() as group:
        for server in servers:
            group.create_task(server.serve_forever())


if __name__ == "__main__":
    asyncio.run(main())
