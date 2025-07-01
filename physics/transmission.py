from config import *

class TransmissionSystem:
    def __init__(self):
        self.current_gear = 1
        
    def get_gear_ratio(self, gear):
        """Get gear ratio for specified gear"""
        if gear == -1:  # Reverse
            return REVERSE_GEAR_RATIO
        return GEAR_RATIOS.get(gear, 1.0)
    
    def calculate_rpm_from_speed(self, speed, gear):
        """Calculate engine RPM from vehicle speed and gear"""
        if gear > 0 and speed > 0.1:
            speed_mps = speed * (1000 / 3600)
            wheel_rps = speed_mps / TIRE_CIRCUMFERENCE
            wheel_rpm = wheel_rps * 60
            gear_ratio = self.get_gear_ratio(gear)
            return max(IDLE_RPM, wheel_rpm * gear_ratio * FINAL_DRIVE_RATIO)
        return IDLE_RPM
    
    def get_acceleration_factor(self, gear):
        """Get acceleration factor for current gear"""
        gear_accel_factors = {1: 1.2, 2: 0.9, 3: 0.7, 4: 0.5, 5: 0.4, 6: 0.35}
        return gear_accel_factors.get(gear, 0.5)
