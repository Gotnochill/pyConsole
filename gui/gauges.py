import tkinter as tk
import math
from utils.constants import *
from config import MAX_SPEED, MAX_RPM

class SpeedGauge:
    def __init__(self, canvas):
        self.canvas = canvas
        
    def draw_gauge_face(self):
        """Draw the speedometer face with tick marks"""
        self.canvas.delete("all")
        # Draw outer circle
        self.canvas.create_oval(
            GAUGE_CENTER_X - GAUGE_RADIUS, GAUGE_CENTER_Y - GAUGE_RADIUS,
            GAUGE_CENTER_X + GAUGE_RADIUS, GAUGE_CENTER_Y + GAUGE_RADIUS,
            outline=GAUGE_OUTLINE_COLOR, width=3
        )
        
        # Draw tick marks and numbers
        for i in range(0, 270, 20):
            angle = math.radians(225 - (i/260 * 270))
            self._draw_tick_mark(angle, i)
            
        # Draw minor ticks
        for i in range(0, 270, 10):
            angle = math.radians(225 - (i/260 * 270))
            self._draw_minor_tick(angle)
            
        # Center label
        self.canvas.create_text(
            GAUGE_CENTER_X, GAUGE_CENTER_Y - 40, 
            text="km/h", fill='white', font=('Arial', 14)
        )
    
    def _draw_tick_mark(self, angle, value):
        """Draw major tick marks with numbers"""
        x1 = GAUGE_CENTER_X + (GAUGE_RADIUS - 15) * math.cos(angle)
        y1 = GAUGE_CENTER_Y - (GAUGE_RADIUS - 15) * math.sin(angle)
        x2 = GAUGE_CENTER_X + GAUGE_RADIUS * math.cos(angle)
        y2 = GAUGE_CENTER_Y - GAUGE_RADIUS * math.sin(angle)
        
        self.canvas.create_line(x1, y1, x2, y2, fill='white', width=2)
        
        if value % 20 == 0:
            num_x = GAUGE_CENTER_X + (GAUGE_RADIUS - 30) * math.cos(angle)
            num_y = GAUGE_CENTER_Y - (GAUGE_RADIUS - 30) * math.sin(angle)
            self.canvas.create_text(
                num_x, num_y, text=str(value),
                fill='white', font=('Arial', 12, 'bold')
            )
    
    def _draw_minor_tick(self, angle):
        """Draw minor tick marks"""
        x1 = GAUGE_CENTER_X + (GAUGE_RADIUS - 8) * math.cos(angle)
        y1 = GAUGE_CENTER_Y - (GAUGE_RADIUS - 8) * math.sin(angle)
        x2 = GAUGE_CENTER_X + GAUGE_RADIUS * math.cos(angle)
        y2 = GAUGE_CENTER_Y - GAUGE_RADIUS * math.sin(angle)
        self.canvas.create_line(x1, y1, x2, y2, fill='white', width=1)
    
    def draw_needle(self, speed):
        """Draw the speedometer needle"""
        self.canvas.delete("speed_needle")
        self.canvas.delete("speed_display")
        
        speed_ratio = min(speed / MAX_SPEED, 1.0)
        angle = math.radians(225 - (speed_ratio * 270))
        
        needle_x = GAUGE_CENTER_X + NEEDLE_LENGTH * math.cos(angle)
        needle_y = GAUGE_CENTER_Y - NEEDLE_LENGTH * math.sin(angle)
        
        self.canvas.create_line(
            GAUGE_CENTER_X, GAUGE_CENTER_Y, needle_x, needle_y,
            fill=NEEDLE_COLOR, width=4, tags="speed_needle"
        )
        
        # Center circle
        self.canvas.create_oval(
            GAUGE_CENTER_X - 8, GAUGE_CENTER_Y - 8,
            GAUGE_CENTER_X + 8, GAUGE_CENTER_Y + 8,
            fill='gray', outline='white', tags="speed_needle"
        )
        
        # Speed display
        self.canvas.create_text(
            GAUGE_CENTER_X, GAUGE_CENTER_Y + 40, text=f"{speed:.1f}",
            fill='white', font=('Arial', 16, 'bold'), tags="speed_display"
        )

class RPMGauge:
    def __init__(self, canvas):
        self.canvas = canvas
        
    def draw_gauge_face(self):
        """Draw the RPM gauge face with tick marks"""
        self.canvas.delete("all")
        # Draw outer circle
        self.canvas.create_oval(
            GAUGE_CENTER_X - GAUGE_RADIUS, GAUGE_CENTER_Y - GAUGE_RADIUS,
            GAUGE_CENTER_X + GAUGE_RADIUS, GAUGE_CENTER_Y + GAUGE_RADIUS,
            outline=GAUGE_OUTLINE_COLOR, width=3
        )
        
        # Draw tick marks and numbers (0-9 for RPM x1000)
        for i in range(0, 10):
            angle = math.radians(225 - (i/9 * 270))
            color = RED_ZONE_COLOR if i >= 7 else 'white'
            self._draw_tick_mark(angle, i, color)
            
        # Center labels
        self.canvas.create_text(
            GAUGE_CENTER_X, GAUGE_CENTER_Y - 40, 
            text="rpm", fill='white', font=('Arial', 14)
        )
        self.canvas.create_text(
            GAUGE_CENTER_X, GAUGE_CENTER_Y - 25, 
            text="x 1000", fill='white', font=('Arial', 10)
        )
    
    def _draw_tick_mark(self, angle, value, color):
        """Draw tick marks with numbers"""
        x1 = GAUGE_CENTER_X + (GAUGE_RADIUS - 15) * math.cos(angle)
        y1 = GAUGE_CENTER_Y - (GAUGE_RADIUS - 15) * math.sin(angle)
        x2 = GAUGE_CENTER_X + GAUGE_RADIUS * math.cos(angle)
        y2 = GAUGE_CENTER_Y - GAUGE_RADIUS * math.sin(angle)
        
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
        
        num_x = GAUGE_CENTER_X + (GAUGE_RADIUS - 30) * math.cos(angle)
        num_y = GAUGE_CENTER_Y - (GAUGE_RADIUS - 30) * math.sin(angle)
        self.canvas.create_text(
            num_x, num_y, text=str(value),
            fill=color, font=('Arial', 12, 'bold')
        )
    
    def draw_needle(self, rpm, odometer):
        """Draw the RPM needle and update displays"""
        self.canvas.delete("rpm_needle")
        self.canvas.delete("rpm_display")
        self.canvas.delete("odometer")
        
        rpm_ratio = min(rpm / MAX_RPM, 1.0)
        angle = math.radians(225 - (rpm_ratio * 270))
        
        needle_x = GAUGE_CENTER_X + NEEDLE_LENGTH * math.cos(angle)
        needle_y = GAUGE_CENTER_Y - NEEDLE_LENGTH * math.sin(angle)
        
        needle_color = RED_ZONE_COLOR if rpm > 7000 else NEEDLE_COLOR
        self.canvas.create_line(
            GAUGE_CENTER_X, GAUGE_CENTER_Y, needle_x, needle_y,
            fill=needle_color, width=4, tags="rpm_needle"
        )
        
        # Center circle
        self.canvas.create_oval(
            GAUGE_CENTER_X - 8, GAUGE_CENTER_Y - 8,
            GAUGE_CENTER_X + 8, GAUGE_CENTER_Y + 8,
            fill='gray', outline='white', tags="rpm_needle"
        )
        
        # RPM display
        self.canvas.create_text(
            GAUGE_CENTER_X, GAUGE_CENTER_Y + 40, text=f"{rpm:.0f}",
            fill='white', font=('Arial', 16, 'bold'), tags="rpm_display"
        )
        
        # Odometer
        self.canvas.create_text(
            GAUGE_CENTER_X + 60, GAUGE_CENTER_Y + 60, text=f"{odometer:.2f}",
            fill='white', font=('Arial', 10), tags="odometer"
        )
