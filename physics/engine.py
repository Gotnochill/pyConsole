import time
from config import *

class EnginePhysics:
    def __init__(self):
        self.velocity = 0.0
        self.acceleration = 0.0
        self.odometer = 0.0
        self.last_time = time.time()
        
    def calculate_rpm(self, speed, gear):
        """Calculate realistic RPM based on speed and gear"""
        if gear > 0 and speed > 0.1:
            speed_mps = speed * (1000 / 3600)
            wheel_rps = speed_mps / TIRE_CIRCUMFERENCE
            wheel_rpm = wheel_rps * 60
            gear_ratio = GEAR_RATIOS.get(gear, 1.0)
            return max(IDLE_RPM, wheel_rpm * gear_ratio * FINAL_DRIVE_RATIO)
        return IDLE_RPM
    
    def calculate_acceleration(self, gas_factor, gear, clutch_factor):
        """Calculate realistic acceleration based on inputs"""
        if gas_factor > 0 and clutch_factor < 70:
            gear_accel_factors = {1: 1.2, 2: 0.9, 3: 0.7, 4: 0.5, 5: 0.4, 6: 0.35}
            accel_factor = gear_accel_factors.get(gear, 0.5)
            return gas_factor * accel_factor * 1.5
        return 0
    
    def update_odometer(self, speed):
        """Update odometer based on current speed"""
        current_time = time.time()
        time_diff = current_time - self.last_time
        if time_diff > 0:
            distance_traveled = (speed / 3600) * time_diff
            self.odometer += distance_traveled
            self.last_time = current_time
