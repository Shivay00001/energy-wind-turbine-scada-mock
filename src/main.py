import logging
import asyncio
from src.scada_server import SCADAServer

logging.basicConfig(level=logging.INFO)

async def main_async():
    server = SCADAServer(port=5020)
    await server.run()

def main():
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        print("SCADA Server stopped.")

if __name__ == "__main__":
    main()
