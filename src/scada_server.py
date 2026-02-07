import logging
import asyncio
from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

from src.turbine_sim import TurbinePhysics

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
        
        # Initialize Datastore
        self.store = ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [0]*100),
            co=ModbusSequentialDataBlock(0, [0]*100),
            hr=ModbusSequentialDataBlock(0, [0]*100),
            ir=ModbusSequentialDataBlock(0, [0]*100))
        
        self.context = ModbusServerContext(slaves=self.store, single=True)

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
                1 # Status Run
            ]
            
            # Write to Holding Registers (Offset 0 = 40001)
            self.store.setValues(3, 0, values)
            
            logging.info(f"Updated Registers: Wind={state['wind_speed']:.1f}m/s Power={state['power_kw']:.0f}kW")
            await asyncio.sleep(1)

    async def run(self):
        logging.info(f"Starting SCADA Server on 0.0.0.0:{self.port}")
        
        # Start update task
        asyncio.create_task(self.update_loop())
        
        # Start Modbus Server
        await StartAsyncTcpServer(context=self.context, address=("0.0.0.0", self.port))
