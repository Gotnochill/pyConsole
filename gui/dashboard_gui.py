import tkinter as tk
from tkinter import messagebox
import threading
import time
from gui.gauges import SpeedGauge, RPMGauge
from gui.controls import DashboardControls
from physics.engine import EnginePhysics
from physics.safety_systems import SafetySystems
from config import *
from utils.constants import BUTTON_COLOR, ACTIVE_COLOR

class CarDashboard:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        
        # Initialize components
        self.engine = EnginePhysics()
        self.safety_systems = SafetySystems()
        
        # Dashboard state
        self.speed = 0.0
        self.rpm = 0.0
        self.target_speed = 0.0
        self.target_rpm = 0.0
        self.steering_angle = 0
        self.clutch = 0
        self.brake = 0
        self.gas = 0
        self.gear = 1
        self.running = False
        self.engine_on = False
        
        # Animation control
        self.animation_running = True
        self.physics_running = False
        self.physics_thread = None
        
        # Setup GUI components
        self.setup_ui()
        self.animate_dashboard()
    
    def setup_window(self):
        """Configure main window"""
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=BACKGROUND_COLOR)
    
    def setup_ui(self):
        """Setup the user interface"""
        # Create main frames
        main_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top frame for gauges
        gauge_frame = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
        gauge_frame.pack(fill=tk.BOTH, expand=True)

        # Speed gauge
        self.speed_canvas = tk.Canvas(
            gauge_frame, width=300, height=300, bg='black', 
            highlightthickness=2, highlightbackground='white'
        )
        self.speed_canvas.pack(side=tk.LEFT, padx=20, pady=20)
        self.speed_gauge = SpeedGauge(self.speed_canvas)

        # RPM gauge
        self.rpm_canvas = tk.Canvas(
            gauge_frame, width=300, height=300, bg='black', 
            highlightthickness=2, highlightbackground='white'
        )
        self.rpm_canvas.pack(side=tk.RIGHT, padx=20, pady=20)
        self.rpm_gauge = RPMGauge(self.rpm_canvas)
        
        # Setup controls with callbacks
        callbacks = {
            'toggle_power': self.toggle_power,
            'toggle_simulation': self.toggle_simulation,
            'reset_dashboard': self.reset_dashboard,
            'toggle_abs': self.toggle_abs,
            'toggle_esp': self.toggle_esp,
            'toggle_acc': self.toggle_acc,
            'toggle_ods': self.toggle_ods,
            'toggle_spd': self.toggle_spd,
            'update_steering': self.update_steering,
            'update_clutch': self.update_clutch,
            'update_brake': self.update_brake,
            'update_gas': self.update_gas,
            'set_gear': self.set_gear
        }
        
        self.controls = DashboardControls(main_frame, callbacks)
        
        # Draw initial gauges
        self.speed_gauge.draw_gauge_face()
        self.rpm_gauge.draw_gauge_face()
        self.highlight_gear('1')
    
    def toggle_power(self):
        """Toggle engine ON/OFF"""
        self.engine_on = not self.engine_on
        if self.engine_on:
            self.controls.power_btn.configure(bg=ACTIVE_COLOR)
            self.controls.engine_status.configure(text="ENGINE ON", bg=ACTIVE_COLOR)
            self.target_rpm = IDLE_RPM
        else:
            self.controls.power_btn.configure(bg=BUTTON_COLOR)
            self.controls.engine_status.configure(text="ENGINE OFF", bg='red')
            self.target_rpm = 0
            if self.running:
                self.toggle_simulation()
    
    def toggle_simulation(self):
        """Toggle driving simulation ON/OFF"""
        if not self.engine_on:
            messagebox.showwarning("Warning", "Please start the engine first!")
            return
        self.running = not self.running
        if self.running:
            self.controls.start_btn.configure(bg=ACTIVE_COLOR)
            self.controls.sim_status.configure(text="SIM ON", bg=ACTIVE_COLOR)
            self.start_physics_simulation()
        else:
            self.controls.start_btn.configure(bg=BUTTON_COLOR)
            self.controls.sim_status.configure(text="SIM OFF", bg='red')
            self.stop_physics_simulation()
            self.target_speed = 0
            self.target_rpm = IDLE_RPM if self.engine_on else 0
    
    def reset_dashboard(self):
        """Reset all dashboard values to default"""
        if self.running:
            self.toggle_simulation()
        if self.engine_on:
            self.toggle_power()
        
        self.speed = 0.0
        self.rpm = 0.0
        self.target_speed = 0.0
        self.target_rpm = 0.0
        self.engine.velocity = 0.0
        self.engine.acceleration = 0.0
        self.steering_angle = 0
        self.clutch = 0
        self.brake = 0
        self.gas = 0
        self.gear = 1
        self.engine.odometer = 0.0
        
        # Reset UI elements
        self.controls.steering_scale.set(0)
        self.controls.clutch_scale.set(0)
        self.controls.brake_scale.set(0)
        self.controls.gas_scale.set(0)
        self.highlight_gear('1')
        
        # Reset button colors
        self.controls.reset_btn.configure(bg='orange')
        self.root.after(200, lambda: self.controls.reset_btn.configure(bg=BUTTON_COLOR))
        
        # Reset safety systems
        self.safety_systems.abs_enabled = False
        self.safety_systems.esp_enabled = False
        self.safety_systems.acc_enabled = False
        self.safety_systems.ods_enabled = False
        self.safety_systems.spd_enabled = False
        
        self.controls.abs_btn.configure(bg=BUTTON_COLOR)
        self.controls.esp_btn.configure(bg=BUTTON_COLOR)
        self.controls.acc_btn.configure(bg=BUTTON_COLOR)
        self.controls.ods_btn.configure(bg=BUTTON_COLOR)
        self.controls.spd_btn.configure(bg=BUTTON_COLOR)
    
    def toggle_abs(self):
        enabled = self.safety_systems.toggle_abs()
        self.controls.abs_btn.configure(bg=ACTIVE_COLOR if enabled else BUTTON_COLOR)
        print(f"ABS {'enabled' if enabled else 'disabled'}")
    
    def toggle_esp(self):
        enabled = self.safety_systems.toggle_esp()
        self.controls.esp_btn.configure(bg=ACTIVE_COLOR if enabled else BUTTON_COLOR)
        print(f"ESP {'enabled' if enabled else 'disabled'}")
    
    def toggle_acc(self):
        enabled = self.safety_systems.toggle_acc()
        self.controls.acc_btn.configure(bg=ACTIVE_COLOR if enabled else BUTTON_COLOR)
        print(f"ACC {'enabled' if enabled else 'disabled'}")
    
    def toggle_ods(self):
        enabled = self.safety_systems.toggle_ods()
        self.controls.ods_btn.configure(bg=ACTIVE_COLOR if enabled else BUTTON_COLOR)
        print(f"ODS {'enabled' if enabled else 'disabled'}")
    
    def toggle_spd(self):
        enabled = self.safety_systems.toggle_spd()
        self.controls.spd_btn.configure(bg=ACTIVE_COLOR if enabled else BUTTON_COLOR)
        print(f"SPD {'enabled' if enabled else 'disabled'}")
    
    def update_steering(self, value):
        self.steering_angle = float(value)
    
    def update_clutch(self, value):
        self.clutch = float(value)
    
    def update_brake(self, value):
        self.brake = float(value)
    
    def update_gas(self, value):
        self.gas = float(value)
    
    def set_gear(self, gear):
        if gear == 'R':
            self.gear = -1
        else:
            self.gear = int(gear)
        self.highlight_gear(gear)
    
    def highlight_gear(self, current_gear):
        """Highlight current gear"""
        for gear, btn in self.controls.gear_buttons.items():
            btn.configure(bg='#6a6a6a')
        if current_gear in self.controls.gear_buttons:
            self.controls.gear_buttons[current_gear].configure(bg='red')
    
    def start_physics_simulation(self):
        """Start the physics simulation in a separate thread"""
        if not self.physics_running:
            self.physics_running = True
            self.physics_thread = threading.Thread(target=self.physics_loop, daemon=True)
            self.physics_thread.start()
    
    def stop_physics_simulation(self):
        """Stop the physics simulation"""
        self.physics_running = False
    
    def physics_loop(self):
        """Realistic physics simulation loop"""
        while self.physics_running:
            if self.engine_on and self.running:
                # Get current input values
                gas_factor = self.gas / 100.0
                brake_factor = self.brake / 100.0
                clutch_factor = self.clutch / 100.0

                # Apply safety systems
                brake_factor = self.safety_systems.apply_abs(brake_factor)
                gas_factor = self.safety_systems.apply_esp(gas_factor, self.steering_angle)
                gas_factor = self.safety_systems.apply_acc(gas_factor, self.speed)
                gas_factor = self.safety_systems.apply_ods(gas_factor)

                if self.gear > 0:  # Forward gear
                    # Calculate RPM based on speed and gear
                    if self.speed > 0.1:
                        self.target_rpm = self.engine.calculate_rpm(self.speed, self.gear)
                    else:
                        if gas_factor > 0:
                            self.target_rpm = IDLE_RPM + (gas_factor * (3500 - IDLE_RPM))
                        else:
                            self.target_rpm = IDLE_RPM

                    # Calculate acceleration
                    if gas_factor > 0 and clutch_factor < 70:
                        self.engine.acceleration = self.engine.calculate_acceleration(
                            gas_factor, self.gear, clutch_factor
                        )
                        if self.speed < MAX_SPEED:
                            self.engine.velocity += self.engine.acceleration
                    else:
                        self.engine.acceleration = 0

                    # Braking
                    if brake_factor > 0:
                        brake_deceleration = brake_factor * 8
                        self.engine.velocity = max(0, self.engine.velocity - brake_deceleration)

                    # Natural deceleration
                    if gas_factor == 0 and brake_factor == 0:
                        natural_decel = 0.5 + (self.speed * 0.02)
                        self.engine.velocity = max(0, self.engine.velocity - natural_decel)

                elif self.gear == -1:  # Reverse gear
                    if self.speed > 0.1:
                        self.target_rpm = self.engine.calculate_rpm(self.speed, self.gear)
                    else:
                        if gas_factor > 0:
                            self.target_rpm = IDLE_RPM + (gas_factor * (2500 - IDLE_RPM))
                        else:
                            self.target_rpm = IDLE_RPM

                    if gas_factor > 0 and clutch_factor < 70:
                        reverse_accel = gas_factor * 1.0
                        if abs(self.engine.velocity) < 40:
                            self.engine.velocity -= reverse_accel

                    if brake_factor > 0:
                        brake_deceleration = brake_factor * 6
                        if self.engine.velocity < 0:
                            self.engine.velocity = min(0, self.engine.velocity + brake_deceleration)

                else:  # Neutral gear
                    if gas_factor > 0:
                        self.target_rpm = IDLE_RPM + (gas_factor * (4000 - IDLE_RPM))
                    else:
                        self.target_rpm = IDLE_RPM
                    
                    self.engine.acceleration = 0
                    natural_decel = 1.0 + (self.speed * 0.03)
                    self.engine.velocity = max(0, self.engine.velocity - natural_decel)

                # Apply speed limiter
                self.engine.velocity = self.safety_systems.apply_speed_limiter(self.engine.velocity)
                self.target_speed = max(0, abs(self.engine.velocity))

                # Update odometer
                self.engine.update_odometer(self.speed)

            elif self.engine_on and not self.running:
                self.target_rpm = IDLE_RPM
                coast_decel = 1.0 + (self.speed * 0.03)
                self.engine.velocity = max(0, self.engine.velocity - coast_decel)
                self.target_speed = max(0, self.engine.velocity)

            else:
                self.target_rpm = 0
                coast_decel = 2.0
                self.engine.velocity = max(0, self.engine.velocity - coast_decel)
                self.target_speed = max(0, self.engine.velocity)

            time.sleep(PHYSICS_UPDATE_RATE)
    
    def animate_dashboard(self):
        """Smooth animation of dashboard elements"""
        if self.animation_running:
            # Smooth speed transition
            speed_diff = self.target_speed - self.speed
            if abs(speed_diff) > 0.1:
                self.speed += speed_diff * 0.1
            else:
                self.speed = self.target_speed

            # Smooth RPM transition
            rpm_diff = self.target_rpm - self.rpm
            if abs(rpm_diff) > 10:
                self.rpm += rpm_diff * 0.15
            else:
                self.rpm = self.target_rpm

            # Update gauge displays
            self.speed_gauge.draw_needle(self.speed)
            self.rpm_gauge.draw_needle(self.rpm, self.engine.odometer)

            # Schedule next animation frame
            self.root.after(GUI_UPDATE_RATE, self.animate_dashboard)
    
    def on_closing(self):
        """Clean shutdown of the application"""
        self.animation_running = False
        self.physics_running = False
        if self.physics_thread and self.physics_thread.is_alive():
            self.physics_thread.join(timeout=1.0)
        self.root.destroy()
