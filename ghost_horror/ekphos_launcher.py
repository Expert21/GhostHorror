"""
Ekphos Launcher for Ghost Horror Mode
Detects terminal and launches Ekphos, monitors for exit
"""

import os
import subprocess
import shutil
from typing import Optional, List


def find_terminal() -> Optional[List[str]]:
    """
    Find an available terminal emulator
    Returns the terminal command with fullscreen flags, or None if not found
    """
    # Terminals in order of preference with fullscreen flags
    # Format: (binary_name, [command, fullscreen_flags..., exec_flag])
    terminals = [
        ("kitty", ["kitty", "--start-as=fullscreen"]),
        ("alacritty", ["alacritty", "--option", "window.startup_mode=Fullscreen", "-e"]),
        ("foot", ["foot", "--fullscreen"]),
        ("wezterm", ["wezterm", "start", "--maximized"]),  # wezterm doesn't have true fullscreen flag
        ("ghostty", ["ghostty", "--fullscreen"]),
        ("konsole", ["konsole", "--fullscreen", "-e"]),
        ("gnome-terminal", ["gnome-terminal", "--full-screen", "--"]),
        ("xfce4-terminal", ["xfce4-terminal", "--fullscreen", "-x"]),
        ("xterm", ["xterm", "-fullscreen", "-e"]),
        ("urxvt", ["urxvt", "-e"]),  # urxvt doesn't have fullscreen flag
        ("st", ["st", "-e"]),  # st doesn't have fullscreen flag
    ]
    
    for name, cmd in terminals:
        if shutil.which(name):
            return cmd
    
    return None


def check_ekphos_installed() -> bool:
    """Check if ekphos is installed"""
    return shutil.which("ekphos") is not None


class EkphosLauncher:
    """Launch and monitor Ekphos"""
    
    def __init__(self):
        self.process: Optional[subprocess.Popen] = None
        self.terminal_cmd: Optional[List[str]] = None
    
    def check_requirements(self) -> tuple[bool, str]:
        """
        Check if all requirements are met
        Returns (success, message)
        """
        if not check_ekphos_installed():
            return False, "Ekphos not found! Install with: cargo install ekphos"
        
        self.terminal_cmd = find_terminal()
        if not self.terminal_cmd:
            return False, "No terminal emulator found!"
        
        return True, f"Ready to launch with {self.terminal_cmd[0]}"
    
    def launch(self, working_dir: Optional[str] = None) -> bool:
        """
        Launch Ekphos in a terminal
        Returns True if launch successful
        """
        if not self.terminal_cmd:
            self.terminal_cmd = find_terminal()
            if not self.terminal_cmd:
                print("Error: No terminal found")
                return False
        
        # Build command: terminal + ekphos
        cmd = self.terminal_cmd + ["ekphos"]
        
        # Set working directory (use home if not specified)
        cwd = working_dir or os.path.expanduser("~")
        
        try:
            # Launch the terminal with ekphos
            self.process = subprocess.Popen(
                cmd,
                cwd=cwd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            print(f"Launched Ekphos with PID {self.process.pid}")
            return True
            
        except Exception as e:
            print(f"Error launching Ekphos: {e}")
            return False
    
    def is_running(self) -> bool:
        """Check if Ekphos is still running"""
        if self.process is None:
            return False
        
        # poll() returns None if process is still running
        return self.process.poll() is None
    
    def wait_for_exit(self) -> int:
        """
        Wait for Ekphos to exit
        Returns the exit code
        """
        if self.process is None:
            return -1
        
        return self.process.wait()
    
    def terminate(self):
        """Force terminate Ekphos if running"""
        if self.process and self.is_running():
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
