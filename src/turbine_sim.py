import math
import random

class TurbinePhysics:
    def __init__(self):
        # Constants for a 2MW Turbine
        self.rho = 1.225 # Air density kg/m^3
        self.radius = 40.0 # Blade radius (m)
        self.area = math.pi * self.radius ** 2
        self.cp = 0.4 # Power coefficient (Betz limit approx)
        self.cut_in = 3.0 # m/s
        self.cut_out = 25.0 # m/s
        self.rated_wind = 12.0 # m/s
        self.max_power = 2000.0 # kW

        # State
        self.wind_speed = 5.0
        self.rotor_speed = 0.0
        self.power_output = 0.0
        self.gearbox_temp = 45.0
    
    def update(self, dt: float = 1.0):
        # Random wind fluctuation
        self.wind_speed += random.uniform(-0.5, 0.5)
        self.wind_speed = max(0.0, min(30.0, self.wind_speed))

        # Calculate Power
        if self.cut_in <= self.wind_speed <= self.cut_out:
            # P = 0.5 * rho * A * v^3 * Cp
            # Result in Watts, convert to kW (divide by 1000)
            raw_power = 0.5 * self.rho * self.area * (self.wind_speed ** 3) * self.cp / 1000.0
            self.power_output = min(raw_power, self.max_power)
            
            # Simple RPM correlation
            self.rotor_speed = (self.wind_speed / self.rated_wind) * 15.0 # Max 15 RPM
        else:
            self.power_output = 0.0
            self.rotor_speed = max(0.0, self.rotor_speed - 0.5) # Spin down

        # Temp simulation
        target_temp = 45.0 + (self.power_output / self.max_power) * 40.0
        self.gearbox_temp += (target_temp - self.gearbox_temp) * 0.1 * dt

    def get_state(self):
        return {
            "wind_speed": self.wind_speed,
            "power_kw": self.power_output,
            "rotor_rpm": self.rotor_speed,
            "gearbox_temp": self.gearbox_temp
        }
