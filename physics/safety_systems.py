from config import *

class SafetySystems:
    def __init__(self):
        self.abs_enabled = False
        self.esp_enabled = False
        self.acc_enabled = False
        self.ods_enabled = False
        self.spd_enabled = False
    
    def apply_abs(self, brake_factor):
        """Apply ABS logic to brake input"""
        if self.abs_enabled and brake_factor > ABS_MAX_BRAKE:
            return ABS_MAX_BRAKE
        return brake_factor
    
    def apply_esp(self, gas_factor, steering_angle):
        """Apply ESP logic to gas input"""
        if self.esp_enabled and abs(steering_angle) > ESP_STEERING_THRESHOLD:
            return gas_factor * ESP_POWER_REDUCTION
        return gas_factor
    
    def apply_acc(self, gas_factor, current_speed):
        """Apply Adaptive Cruise Control"""
        if self.acc_enabled:
            if current_speed < ACC_TARGET_SPEED:
                return min(gas_factor + 0.02, 1.0)
            elif current_speed > ACC_TARGET_SPEED:
                return max(gas_factor - 0.02, 0)
        return gas_factor
    
    def apply_speed_limiter(self, velocity):
        """Apply speed limiter"""
        if self.spd_enabled and velocity > SPD_MAX_SPEED:
            return SPD_MAX_SPEED
        return velocity
    
    def apply_ods(self, gas_factor):
        """Apply Obstacle Detection System"""
        if self.ods_enabled:
            return gas_factor * ODS_POWER_REDUCTION
        return gas_factor
    
    def toggle_abs(self):
        self.abs_enabled = not self.abs_enabled
        return self.abs_enabled
    
    def toggle_esp(self):
        self.esp_enabled = not self.esp_enabled
        return self.esp_enabled
    
    def toggle_acc(self):
        self.acc_enabled = not self.acc_enabled
        return self.acc_enabled
    
    def toggle_ods(self):
        self.ods_enabled = not self.ods_enabled
        return self.ods_enabled
    
    def toggle_spd(self):
        self.spd_enabled = not self.spd_enabled
        return self.spd_enabled
