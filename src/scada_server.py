import logging
import asyncio
from pymodbus.server import ModbusTcpServer
from pymodbus.simulator.simdata import SimData, DataType
from pymodbus.simulator.simdevice import SimDevice

from turbine_sim import TurbinePhysics

# Register Map
# 40001: Wind Speed (x10)
# 40002: Power Output (kW)
# 40003: Rotor RPM (x10)
# 40004: Gearbox Temp (x10)
# 40005: Status (1=Run, 0=Stop, 2=Fault)

class SCADAServer:
    def __init__(self, port=5020):
        self.port = port
        self.sim = TurbinePhysics()

        # 100 holding registers (40001-40100), zero-initialized
        simdata = [SimData(address=0, count=100, values=0, datatype=DataType.REGISTERS)]
        self.device = SimDevice(id=0, simdata=simdata)
        self.core = None  # set in run(); shared SimCore used by the server

    async def update_loop(self):
        """Updates Modbus registers with simulation data."""
        while True:
            self.sim.update()
            state = self.sim.get_state()

            # Map to Registers (Integer Scaling)
            values = [
                int(state["wind_speed"] * 10),
                int(state["power_kw"]),
                int(state["rotor_rpm"] * 10),
                int(state["gearbox_temp"] * 10),
                1  # Status Run
            ]

            # Write to Holding Registers (address 0 = 40001), func_code 16
            await self.core.async_setValues(0, 16, 0, values)

            logging.info(f"Updated Registers: Wind={state['wind_speed']:.1f}m/s Power={state['power_kw']:.0f}kW")
            await asyncio.sleep(1)

    async def run(self):
        logging.info(f"Starting SCADA Server on 0.0.0.0:{self.port}")

        # Build the server first so update_loop writes through the same SimCore
        # (and therefore the same register state) that the server reads.
        server = ModbusTcpServer(self.device, address=("0.0.0.0", self.port))
        self.core = server.context

        # Start update task
        asyncio.create_task(self.update_loop())

        # Start Modbus Server
        await server.serve_forever()
