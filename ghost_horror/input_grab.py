"""
Keyboard Input Grab for Ghost Horror Mode
X11-only implementation for keyboard suppression
"""

import os
import subprocess
from typing import Optional


def is_x11() -> bool:
    """Check if running on X11"""
    session_type = os.environ.get('XDG_SESSION_TYPE', '').lower()
    wayland_display = os.environ.get('WAYLAND_DISPLAY', '')
    
    if wayland_display:
        return False
    if session_type == 'x11':
        return True
    if session_type == 'wayland':
        return False
    
    # Fallback: check for DISPLAY
    return bool(os.environ.get('DISPLAY'))


class X11KeyboardGrab:
    """
    X11 keyboard grab using python-xlib
    Prevents window manager shortcuts during the horror sequence
    """
    
    def __init__(self):
        self.display = None
        self.root = None
        self.grabbed = False
    
    def grab(self) -> bool:
        """
        Grab the keyboard to prevent WM shortcuts
        Returns True if successful
        """
        try:
            from Xlib import X, XK
            from Xlib.display import Display
            
            self.display = Display()
            self.root = self.display.screen().root
            
            # Grab the keyboard
            status = self.root.grab_keyboard(
                True,  # owner_events
                X.GrabModeAsync,  # pointer_mode
                X.GrabModeAsync,  # keyboard_mode
                X.CurrentTime
            )
            
            self.display.sync()
            self.grabbed = (status == X.GrabSuccess)
            return self.grabbed
            
        except ImportError:
            print("Warning: python-xlib not installed, keyboard grab disabled")
            return False
        except Exception as e:
            print(f"Warning: Failed to grab keyboard: {e}")
            return False
    
    def ungrab(self):
        """Release the keyboard grab"""
        if self.grabbed and self.display:
            try:
                from Xlib import X
                self.display.ungrab_keyboard(X.CurrentTime)
                self.display.sync()
                self.grabbed = False
            except Exception as e:
                print(f"Warning: Failed to ungrab keyboard: {e}")
        
        if self.display:
            try:
                self.display.close()
            except:
                pass
            self.display = None


class InputManager:
    """
    Unified input manager
    Currently X11-only, structured for future Wayland support
    """
    
    def __init__(self):
        self.x11_grab: Optional[X11KeyboardGrab] = None
        self.grabbed = False
    
    def grab_keyboard(self) -> bool:
        """
        Attempt to grab the keyboard
        Returns True if successful
        """
        if not is_x11():
            print("Warning: Not running on X11, keyboard suppression disabled")
            print("         (Wayland support coming in a future update)")
            return False
        
        self.x11_grab = X11KeyboardGrab()
        self.grabbed = self.x11_grab.grab()
        
        if self.grabbed:
            print("Keyboard grabbed successfully")
        else:
            print("Warning: Could not grab keyboard")
        
        return self.grabbed
    
    def release_keyboard(self):
        """Release the keyboard grab"""
        if self.x11_grab:
            self.x11_grab.ungrab()
            self.x11_grab = None
        self.grabbed = False
        print("Keyboard released")
    
    def is_grabbed(self) -> bool:
        """Check if keyboard is currently grabbed"""
        return self.grabbed
