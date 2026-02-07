# Energy Wind Turbine SCADA Mock

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB.svg)](https://www.python.org/)
[![Modbus](https://img.shields.io/badge/Protocol-Modbus_TCP-blue.svg)](https://modbus.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A **production-grade SCADA (Supervisory Control and Data Acquisition) simulation** for Wind Turbines. This repository mocks a Modbus TCP server that exposes real-time turbine telemetry based on physics simulations (Wind Speed vs Power Curve), allowing testing of HMI and control systems.

## 🚀 Features

- **Physics Simulation**: Calculates power output using the aerodynamic power equation ($P = 0.5 \rho A v^3 C_p$).
- **Modbus TCP Server**: Exposes telemetry (Wind Speed, RPM, Power, Temperature) via standard Modbus registers.
- **Fault Injection**: Simulates over-speed and over-temperature conditions.
- **Tag Mapping**: Documentation of Holding Registers for SCADA integration.

## 📁 Project Structure

```
energy-wind-turbine-scada-mock/
├── src/
│   ├── scada_server.py   # Modbus Server Logic
│   ├── turbine_sim.py    # Physics Engine
│   └── main.py           # CLI Entrypoint
├── requirements.txt
└── Dockerfile
```

## 🛠️ Quick Start

```bash
# Clone
git clone https://github.com/Shivay00001/energy-wind-turbine-scada-mock.git

# Install
pip install -r requirements.txt

# Run SCADA Server (Port 5020)
python src/main.py
```

## 📄 License

MIT License
