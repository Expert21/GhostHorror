"""
Visual Effects for Ghost Horror Mode
Blood writing animation and glowing eyes
"""

import pygame
import math
import os
from typing import Optional


# Purple glow color palette
PURPLE_GLOW = (138, 43, 226)  # BlueViolet
PURPLE_DARK = (75, 0, 130)    # Indigo
BLOOD_RED = (139, 0, 0)       # Dark red for blood text
BLOOD_DRIP = (100, 0, 0)      # Darker for drip effect


def get_horror_font(size: int) -> pygame.font.Font:
    """
    Get a horror-style font, falls back to system font if needed
    Uses a bold, creepy-looking font
    """
    # Try to find a good horror font
    horror_fonts = [
        "Creepster",
        "Nosifer",
        "Butcherman",
        "Eater",
        "Metal Mania",
        "Creepy",
        "Impact",  # Fallback - bold and readable
    ]
    
    for font_name in horror_fonts:
        try:
            font = pygame.font.SysFont(font_name, size)
            # Test if font actually loaded (not default)
            if font.get_height() > 0:
                return font
        except:
            continue
    
    # Ultimate fallback
    return pygame.font.Font(None, size)


class BloodText:
    """Animated blood-dripping text effect"""
    
    def __init__(self, display, text: str, font_scale: float = 0.15):
        self.display = display
        self.text = text
        self.font_size = display.get_font_size(font_scale)
        self.font = get_horror_font(self.font_size)
        
        # Animation state
        self.chars_revealed = 0
        self.char_progress = 0.0  # 0-1 for current char animation
        self.drips = []  # List of active drip animations
        
        # Timing
        self.char_delay_ms = 150  # Time per character
        self.last_char_time = 0
    
    def render_char(self, char: str, alpha: int = 255) -> pygame.Surface:
        """Render a single character with blood color"""
        # Create text surface
        text_surface = self.font.render(char, True, BLOOD_RED)
        
        # Apply alpha
        if alpha < 255:
            text_surface.set_alpha(alpha)
        
        return text_surface
    
    def get_text_width(self, text: str) -> int:
        """Get the pixel width of text"""
        return self.font.size(text)[0]
    
    def draw(self, surface: pygame.Surface, center_x: int, center_y: int) -> bool:
        """
        Draw the blood text animation
        Returns True when animation is complete
        """
        current_time = pygame.time.get_ticks()
        
        # Progress character reveal
        if self.chars_revealed < len(self.text):
            if current_time - self.last_char_time >= self.char_delay_ms:
                self.chars_revealed += 1
                self.last_char_time = current_time
                
                # Add a drip for some characters
                if self.chars_revealed > 0 and self.text[self.chars_revealed - 1] != ' ':
                    if self.chars_revealed % 2 == 0:  # Every other char gets a drip
                        self._add_drip(self.chars_revealed - 1, center_x, center_y)
        
        # Calculate starting position for centered text
        total_width = self.get_text_width(self.text[:self.chars_revealed])
        start_x = center_x - self.get_text_width(self.text) // 2
        current_x = start_x
        
        # Draw revealed characters
        for i in range(self.chars_revealed):
            char = self.text[i]
            char_surface = self.render_char(char)
            
            # Add slight waviness for creepy effect
            y_offset = int(math.sin(current_time / 200 + i) * 2)
            
            surface.blit(char_surface, (current_x, center_y - self.font_size // 2 + y_offset))
            current_x += self.font.size(char)[0]
        
        # Draw and update drips
        self._update_drips(surface)
        
        return self.chars_revealed >= len(self.text)
    
    def _add_drip(self, char_index: int, center_x: int, center_y: int):
        """Add a blood drip animation at character position"""
        # Calculate x position for this character
        text_before = self.text[:char_index]
        start_x = center_x - self.get_text_width(self.text) // 2
        x = start_x + self.get_text_width(text_before) + self.font.size(self.text[char_index])[0] // 2
        
        self.drips.append({
            'x': x,
            'y': center_y + self.font_size // 2,
            'speed': 2,
            'size': 4,
            'alpha': 255
        })
    
    def _update_drips(self, surface: pygame.Surface):
        """Update and draw blood drips"""
        for drip in self.drips[:]:
            # Draw drip
            drip_color = (*BLOOD_DRIP[:3], drip['alpha']) if drip['alpha'] < 255 else BLOOD_DRIP
            pygame.draw.circle(surface, BLOOD_DRIP, (int(drip['x']), int(drip['y'])), drip['size'])
            
            # Update drip
            drip['y'] += drip['speed']
            drip['size'] = max(1, drip['size'] - 0.02)
            drip['alpha'] = max(0, drip['alpha'] - 2)
            
            # Remove faded drips
            if drip['alpha'] <= 0 or drip['y'] > self.display.screen_height:
                self.drips.remove(drip)


class GlowingEyes:
    """Purple glowing eyes that fade in, breathe, and fade out"""
    
    def __init__(self, display, size_scale: float = 0.08):
        self.display = display
        self.eye_size = int(display.screen_height * size_scale)
        self.spacing = int(self.eye_size * 2.5)  # Space between eyes
        
        # Animation state
        self.state = 'fade_in'  # fade_in, breathing, fade_out
        self.alpha = 0
        self.breath_phase = 0
        self.state_start_time = 0
        
        # Timing (ms)
        self.fade_in_duration = 1000
        self.breathing_duration = 2000
        self.fade_out_duration = 500
        
        # Create eye surfaces
        self._create_eye_surfaces()
    
    def _create_eye_surfaces(self):
        """Create the glowing eye sprites"""
        # Main eye surface with glow
        size = self.eye_size * 3  # Extra space for glow
        self.eye_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        center = size // 2
        
        # Outer glow layers
        for i in range(5, 0, -1):
            glow_size = self.eye_size // 2 + i * 8
            glow_alpha = 50 - i * 8
            glow_color = (*PURPLE_GLOW, max(0, glow_alpha))
            pygame.draw.circle(self.eye_surface, glow_color, (center, center), glow_size)
        
        # Main eye (bright center)
        pygame.draw.circle(self.eye_surface, PURPLE_GLOW, (center, center), self.eye_size // 2)
        
        # Inner bright core
        core_color = (200, 150, 255)  # Lighter purple
        pygame.draw.circle(self.eye_surface, core_color, (center, center), self.eye_size // 4)
        
        # Pupil (dark center)
        pygame.draw.circle(self.eye_surface, (20, 0, 30), (center, center), self.eye_size // 8)
    
    def start(self):
        """Start the animation sequence"""
        self.state = 'fade_in'
        self.state_start_time = pygame.time.get_ticks()
        self.alpha = 0
    
    def update(self) -> bool:
        """
        Update animation state
        Returns True when animation is complete (after fade out)
        """
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.state_start_time
        
        if self.state == 'fade_in':
            progress = min(1.0, elapsed / self.fade_in_duration)
            self.alpha = int(255 * progress)
            
            if progress >= 1.0:
                self.state = 'breathing'
                self.state_start_time = current_time
        
        elif self.state == 'breathing':
            # Breathing effect: subtle scale/alpha pulse
            self.breath_phase = (elapsed / 500) * math.pi  # Complete cycle every 500ms
            breath_mod = 0.1 * math.sin(self.breath_phase)
            self.alpha = int(255 * (0.9 + breath_mod))
            
            if elapsed >= self.breathing_duration:
                self.state = 'fade_out'
                self.state_start_time = current_time
        
        elif self.state == 'fade_out':
            progress = min(1.0, elapsed / self.fade_out_duration)
            self.alpha = int(255 * (1.0 - progress))
            
            if progress >= 1.0:
                return True  # Animation complete
        
        return False
    
    def draw(self, surface: pygame.Surface):
        """Draw the eyes on the surface"""
        if self.alpha <= 0:
            return
        
        center_x, center_y = self.display.get_center()
        
        # Apply breathing scale effect
        scale = 1.0
        if self.state == 'breathing':
            scale = 1.0 + 0.05 * math.sin(self.breath_phase)
        
        # Scale eye surface
        scaled_size = int(self.eye_surface.get_width() * scale)
        scaled_eye = pygame.transform.scale(self.eye_surface, (scaled_size, scaled_size))
        scaled_eye.set_alpha(self.alpha)
        
        # Draw left eye
        left_x = center_x - self.spacing // 2 - scaled_size // 2
        left_y = center_y - scaled_size // 2
        surface.blit(scaled_eye, (left_x, left_y))
        
        # Draw right eye
        right_x = center_x + self.spacing // 2 - scaled_size // 2
        right_y = center_y - scaled_size // 2
        surface.blit(scaled_eye, (right_x, right_y))


class TextInput:
    """Simple text input for the exit sequence"""
    
    def __init__(self, display, prompt: str, font_scale: float = 0.06):
        self.display = display
        self.prompt = prompt
        self.font_size = display.get_font_size(font_scale)
        self.font = pygame.font.Font(None, self.font_size)
        self.input_text = ""
        self.cursor_visible = True
        self.cursor_timer = 0
    
    def handle_event(self, event) -> Optional[str]:
        """
        Handle keyboard events
        Returns the input text if Enter is pressed, None otherwise
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return self.input_text.strip().lower()
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.unicode.isprintable():
                self.input_text += event.unicode
        return None
    
    def draw(self, surface: pygame.Surface):
        """Draw the prompt and input field"""
        center_x, center_y = self.display.get_center()
        
        # Update cursor blink
        current_time = pygame.time.get_ticks()
        if current_time - self.cursor_timer > 500:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = current_time
        
        # Draw prompt (purple glow color)
        prompt_surface = self.font.render(self.prompt, True, PURPLE_GLOW)
        prompt_x = center_x - prompt_surface.get_width() // 2
        prompt_y = center_y - self.font_size
        surface.blit(prompt_surface, (prompt_x, prompt_y))
        
        # Draw input text with cursor
        display_text = self.input_text
        if self.cursor_visible:
            display_text += "_"
        
        input_surface = self.font.render(display_text, True, (255, 255, 255))
        input_x = center_x - input_surface.get_width() // 2
        input_y = center_y + 10
        surface.blit(input_surface, (input_x, input_y))


class MessageDisplay:
    """Display a message with fade in/out"""
    
    def __init__(self, display, message: str, color: tuple = PURPLE_GLOW, font_scale: float = 0.08):
        self.display = display
        self.message = message
        self.color = color
        self.font_size = display.get_font_size(font_scale)
        self.font = get_horror_font(self.font_size)
        self.alpha = 0
    
    def show(self, duration_ms: int = 2000, fade_in_ms: int = 500, fade_out_ms: int = 500):
        """Show the message with fade in and out"""
        start_time = pygame.time.get_ticks()
        total_duration = fade_in_ms + duration_ms + fade_out_ms
        
        while pygame.time.get_ticks() - start_time < total_duration:
            elapsed = pygame.time.get_ticks() - start_time
            
            # Calculate alpha based on phase
            if elapsed < fade_in_ms:
                self.alpha = int(255 * (elapsed / fade_in_ms))
            elif elapsed < fade_in_ms + duration_ms:
                self.alpha = 255
            else:
                fade_elapsed = elapsed - fade_in_ms - duration_ms
                self.alpha = int(255 * (1 - fade_elapsed / fade_out_ms))
            
            self.display.clear()
            self.draw(self.display.screen)
            self.display.update()
            
            if not self.display.running:
                break
    
    def draw(self, surface: pygame.Surface):
        """Draw the message"""
        center_x, center_y = self.display.get_center()
        
        text_surface = self.font.render(self.message, True, self.color)
        text_surface.set_alpha(self.alpha)
        
        x = center_x - text_surface.get_width() // 2
        y = center_y - text_surface.get_height() // 2
        surface.blit(text_surface, (x, y))
