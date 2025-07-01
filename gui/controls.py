import tkinter as tk
from config import BACKGROUND_COLOR
from utils.constants import BUTTON_COLOR, ACTIVE_COLOR

class DashboardControls:
    def __init__(self, parent, callbacks):
        self.parent = parent
        self.callbacks = callbacks
        self.setup_controls()
    
    def setup_controls(self):
        """Setup all control widgets"""
        self.setup_system_buttons()
        self.setup_status_indicators()
        self.setup_steering()
        self.setup_pedals()
        self.setup_gearbox()
    
    def setup_system_buttons(self):
        """Create system control buttons"""
        # Controls frame
        controls_frame = tk.Frame(self.parent, bg=BACKGROUND_COLOR)
        controls_frame.pack(fill=tk.X, pady=20)

        # Left controls
        left_controls = tk.Frame(controls_frame, bg=BACKGROUND_COLOR)
        left_controls.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # System buttons
        button_frame = tk.Frame(left_controls, bg=BACKGROUND_COLOR)
        button_frame.pack(anchor=tk.W, pady=10)

        # Power button
        self.power_btn = tk.Button(
            button_frame, text="ENGINE\nON/OFF", bg=BUTTON_COLOR, fg='white', 
            font=('Arial', 9, 'bold'), width=8, height=2, 
            command=self.callbacks['toggle_power']
        )
        self.power_btn.grid(row=0, column=0, padx=5, pady=2)

        # Start/Stop button
        self.start_btn = tk.Button(
            button_frame, text="START\nSIM", bg=BUTTON_COLOR, fg='white', 
            font=('Arial', 9, 'bold'), width=8, height=2, 
            command=self.callbacks['toggle_simulation']
        )
        self.start_btn.grid(row=0, column=1, padx=5, pady=2)

        # Reset button
        self.reset_btn = tk.Button(
            button_frame, text="RESET", bg=BUTTON_COLOR, fg='white', 
            font=('Arial', 10, 'bold'), width=8, height=2, 
            command=self.callbacks['reset_dashboard']
        )
        self.reset_btn.grid(row=0, column=2, padx=5, pady=2)

        # Safety system buttons
        self.abs_btn = tk.Button(
            button_frame, text="ABS", bg=BUTTON_COLOR, fg='white', 
            font=('Arial', 10, 'bold'), width=6, height=2, 
            command=self.callbacks['toggle_abs']
        )
        self.abs_btn.grid(row=1, column=0, padx=5, pady=2)

        self.esp_btn = tk.Button(
            button_frame, text="ESP", bg=BUTTON_COLOR, fg='white', 
            font=('Arial', 10, 'bold'), width=6, height=2, 
            command=self.callbacks['toggle_esp']
        )
        self.esp_btn.grid(row=1, column=1, padx=5, pady=2)

        self.acc_btn = tk.Button(
            button_frame, text="ACC", bg=BUTTON_COLOR, fg='white', 
            font=('Arial', 10, 'bold'), width=6, height=2, 
            command=self.callbacks['toggle_acc']
        )
        self.acc_btn.grid(row=1, column=2, padx=5, pady=2)

        self.ods_btn = tk.Button(
            button_frame, text="ODS", bg=BUTTON_COLOR, fg='white', 
            font=('Arial', 10, 'bold'), width=6, height=2, 
            command=self.callbacks['toggle_ods']
        )
        self.ods_btn.grid(row=2, column=0, padx=5, pady=2)

        self.spd_btn = tk.Button(
            button_frame, text="SPD", bg=BUTTON_COLOR, fg='white', 
            font=('Arial', 10, 'bold'), width=6, height=2, 
            command=self.callbacks['toggle_spd']
        )
        self.spd_btn.grid(row=2, column=1, padx=5, pady=2)

        # Settings button
        tk.Button(
            button_frame, text="SET", bg=BUTTON_COLOR, fg='white', 
            font=('Arial', 10, 'bold'), width=6, height=2
        ).grid(row=2, column=2, padx=5, pady=2)

        # Store references for later access
        self.controls_frame = controls_frame
        self.left_controls = left_controls
    
    def setup_status_indicators(self):
        """Create status indicator labels"""
        status_frame = tk.Frame(self.left_controls, bg=BACKGROUND_COLOR)
        status_frame.pack(anchor=tk.W, pady=10)

        tk.Label(
            status_frame, text="Status:", bg=BACKGROUND_COLOR, fg='white', 
            font=('Arial', 12, 'bold')
        ).pack(side=tk.LEFT)
        
        self.engine_status = tk.Label(
            status_frame, text="ENGINE OFF", bg='red', fg='white', 
            font=('Arial', 10, 'bold'), padx=10
        )
        self.engine_status.pack(side=tk.LEFT, padx=5)
        
        self.sim_status = tk.Label(
            status_frame, text="SIM OFF", bg='red', fg='white', 
            font=('Arial', 10, 'bold'), padx=10
        )
        self.sim_status.pack(side=tk.LEFT, padx=5)
    
    def setup_steering(self):
        """Create steering wheel control"""
        center_controls = tk.Frame(self.controls_frame, bg=BACKGROUND_COLOR)
        center_controls.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)

        tk.Label(
            center_controls, text="Steering Wheel Angle [deg]", 
            bg=BACKGROUND_COLOR, fg='white', font=('Arial', 12)
        ).pack()
        
        steering_frame = tk.Frame(center_controls, bg=BACKGROUND_COLOR)
        steering_frame.pack(pady=10)
        
        self.steering_scale = tk.Scale(
            steering_frame, from_=-550, to=550, orient=tk.HORIZONTAL,
            bg=BACKGROUND_COLOR, fg='white', font=('Arial', 10),
            length=400, command=self.callbacks['update_steering']
        )
        self.steering_scale.pack()

        self.center_controls = center_controls
    
    def setup_pedals(self):
        """Create pedal controls"""
        pedal_frame = tk.Frame(self.center_controls, bg=BACKGROUND_COLOR)
        pedal_frame.pack(pady=20)

        # Clutch
        clutch_frame = tk.Frame(pedal_frame, bg=BACKGROUND_COLOR)
        clutch_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(
            clutch_frame, text="Clutch", bg=BACKGROUND_COLOR, fg='white', 
            font=('Arial', 12)
        ).pack()
        self.clutch_scale = tk.Scale(
            clutch_frame, from_=100, to=0, orient=tk.VERTICAL,
            bg=BACKGROUND_COLOR, fg='white', font=('Arial', 10),
            length=150, command=self.callbacks['update_clutch']
        )
        self.clutch_scale.pack()
        tk.Label(
            clutch_frame, text="%", bg=BACKGROUND_COLOR, fg='white', 
            font=('Arial', 10)
        ).pack()

        # Brake
        brake_frame = tk.Frame(pedal_frame, bg=BACKGROUND_COLOR)
        brake_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(
            brake_frame, text="Brake", bg=BACKGROUND_COLOR, fg='white', 
            font=('Arial', 12)
        ).pack()
        self.brake_scale = tk.Scale(
            brake_frame, from_=100, to=0, orient=tk.VERTICAL,
            bg=BACKGROUND_COLOR, fg='white', font=('Arial', 10),
            length=150, command=self.callbacks['update_brake']
        )
        self.brake_scale.pack()
        tk.Label(
            brake_frame, text="%", bg=BACKGROUND_COLOR, fg='white', 
            font=('Arial', 10)
        ).pack()

        # Gas
        gas_frame = tk.Frame(pedal_frame, bg=BACKGROUND_COLOR)
        gas_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(
            gas_frame, text="Gas", bg=BACKGROUND_COLOR, fg='white', 
            font=('Arial', 12)
        ).pack()
        self.gas_scale = tk.Scale(
            gas_frame, from_=100, to=0, orient=tk.VERTICAL,
            bg=BACKGROUND_COLOR, fg='white', font=('Arial', 10),
            length=150, command=self.callbacks['update_gas']
        )
        self.gas_scale.pack()
        tk.Label(
            gas_frame, text="%", bg=BACKGROUND_COLOR, fg='white', 
            font=('Arial', 10)
        ).pack()
    
    def setup_gearbox(self):
        """Create gearbox controls"""
        right_controls = tk.Frame(self.controls_frame, bg=BACKGROUND_COLOR)
        right_controls.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Label(
            right_controls, text="Gearbox", bg=BACKGROUND_COLOR, fg='white', 
            font=('Arial', 14, 'bold')
        ).pack()

        # Gear display
        self.gear_frame = tk.Frame(right_controls, bg=BUTTON_COLOR, relief=tk.RAISED, bd=2)
        self.gear_frame.pack(pady=10, padx=10)

        # Gear buttons
        gear_positions = [
            [None, '1', None, '3', '5'],
            ['R', None, '2', None, None],
            [None, None, '4', None, '6']
        ]
        self.gear_buttons = {}
        for row, gears in enumerate(gear_positions):
            for col, gear in enumerate(gears):
                if gear:
                    btn = tk.Button(
                        self.gear_frame, text=gear, font=('Arial', 14, 'bold'),
                        width=3, height=2, bg='#6a6a6a', fg='white',
                        command=lambda g=gear: self.callbacks['set_gear'](g)
                    )
                    btn.grid(row=row, column=col, padx=2, pady=2)
                    self.gear_buttons[gear] = btn
