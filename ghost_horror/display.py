"""
Display Engine for Ghost Horror Mode
Handles fullscreen overlay and rendering using Pygame/SDL2
"""

import pygame
import os
from typing import Callable, Optional


class Display:
    """Fullscreen display manager for X11"""
    
    def __init__(self, background_color: tuple = (0, 0, 0)):
        """Initialize the display engine"""
        # Force SDL to use X11
        os.environ['SDL_VIDEODRIVER'] = 'x11'
        
        pygame.init()
        pygame.mixer.quit()  # Disable sound for now (can re-enable later)
        
        # Get display info for scaling
        display_info = pygame.display.Info()
        self.screen_width = display_info.current_w
        self.screen_height = display_info.current_h
        
        # Create fullscreen window
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height),
            pygame.FULLSCREEN | pygame.NOFRAME
        )
        pygame.display.set_caption("Ghost Horror")
        pygame.mouse.set_visible(False)
        
        self.background_color = background_color
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Clear to black immediately
        self.clear()
        pygame.display.flip()
    
    def clear(self, color: Optional[tuple] = None):
        """Clear the screen with background color"""
        self.screen.fill(color or self.background_color)
    
    def get_center(self) -> tuple:
        """Get screen center coordinates"""
        return (self.screen_width // 2, self.screen_height // 2)
    
    def get_font_size(self, scale: float = 0.1) -> int:
        """Get font size scaled to screen height"""
        return int(self.screen_height * scale)
    
    def update(self):
        """Update display and handle events"""
        pygame.display.flip()
        self.clock.tick(60)
        
        # Handle quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def fade_to_black(self, duration_ms: int = 1000):
        """Fade current screen to black"""
        # Capture current screen
        current = self.screen.copy()
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill((0, 0, 0))
        
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < duration_ms:
            progress = (pygame.time.get_ticks() - start_time) / duration_ms
            alpha = int(255 * progress)
            
            self.screen.blit(current, (0, 0))
            overlay.set_alpha(alpha)
            self.screen.blit(overlay, (0, 0))
            
            self.update()
            if not self.running:
                break
        
        self.clear()
        self.update()
    
    def fade_from_black(self, target_surface: pygame.Surface, duration_ms: int = 1000):
        """Fade from black to a target surface"""
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < duration_ms:
            progress = (pygame.time.get_ticks() - start_time) / duration_ms
            alpha = int(255 * progress)
            
            self.clear()
            target_surface.set_alpha(alpha)
            
            # Center the surface
            x = (self.screen_width - target_surface.get_width()) // 2
            y = (self.screen_height - target_surface.get_height()) // 2
            self.screen.blit(target_surface, (x, y))
            
            self.update()
            if not self.running:
                break
    
    def wait(self, duration_ms: int):
        """Wait while keeping display responsive"""
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < duration_ms:
            self.update()
            if not self.running:
                break
    
    def close(self):
        """Close the display"""
        pygame.mouse.set_visible(True)
        pygame.quit()


class SoundManager:
    """
    Sound manager stub for future audio support
    Structured for easy addition of sound effects later
    """
    
    def __init__(self):
        self.enabled = False
        self.sounds = {}
    
    def load(self, name: str, path: str):
        """Load a sound file (stub)"""
        if self.enabled:
            # TODO: pygame.mixer.Sound(path)
            pass
    
    def play(self, name: str, loop: bool = False):
        """Play a loaded sound (stub)"""
        if self.enabled and name in self.sounds:
            # TODO: self.sounds[name].play()
            pass
    
    def stop(self, name: str):
        """Stop a playing sound (stub)"""
        pass
    
    def stop_all(self):
        """Stop all sounds (stub)"""
        pass
