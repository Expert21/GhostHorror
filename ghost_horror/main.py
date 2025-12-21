#!/usr/bin/env python3
"""
Ghost Horror Mode - Main Entry Point
A spooky fullscreen experience before launching Ekphos
"""

import pygame
import time
import sys
from .display import Display, SoundManager
from .effects import BloodText, GlowingEyes, TextInput, MessageDisplay, PURPLE_GLOW, BLOOD_RED
from .input_grab import InputManager, is_x11
from .ekphos_launcher import EkphosLauncher


def run_intro_sequence(display: Display):
    """Run the intro horror sequence"""
    # Phase 1: Black screen pause
    display.clear()
    display.update()
    display.wait(1000)
    
    # Phase 2: Blood writing "You Are Alone"
    blood_text = BloodText(display, "You Are Alone", font_scale=0.12)
    center_x, center_y = display.get_center()
    
    animation_complete = False
    while not animation_complete and display.running:
        display.clear()
        animation_complete = blood_text.draw(display.screen, center_x, center_y)
        display.update()
    
    # Hold the text for a moment
    display.wait(1500)
    
    # Phase 3: Fade to black
    display.fade_to_black(800)
    display.wait(500)
    
    # Phase 4: Glowing eyes
    eyes = GlowingEyes(display, size_scale=0.08)
    eyes.start()
    
    eyes_complete = False
    while not eyes_complete and display.running:
        display.clear()
        eyes_complete = eyes.update()
        eyes.draw(display.screen)
        display.update()
    
    # Final black before Ekphos
    display.clear()
    display.update()


def run_exit_sequence(display: Display) -> bool:
    """
    Run the exit sequence with prompt
    Returns True if user wants to exit, False to relaunch Ekphos
    """
    # Show prompt
    text_input = TextInput(display, "You want to see the light?", font_scale=0.06)
    
    result = None
    while result is None and display.running:
        display.clear()
        text_input.draw(display.screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display.running = False
            elif event.type == pygame.KEYDOWN:
                # ESC key = emergency exit
                if event.key == pygame.K_ESCAPE:
                    return True
                else:
                    result = text_input.handle_event(event)
        
        display.update()
    
    if not display.running:
        return True  # Exit on quit
    
    # Check response
    if result and result.lower() in ['yes', 'y', 'yeah', 'yea', 'yep']:
        # User said yes - show farewell and exit
        message = MessageDisplay(display, "You live to see another day...", PURPLE_GLOW, font_scale=0.08)
        message.show(duration_ms=2500, fade_in_ms=800, fade_out_ms=800)
        return True
    else:
        # User said no or something else - back to Ekphos
        message = MessageDisplay(display, "Then Return!", BLOOD_RED, font_scale=0.10)
        message.show(duration_ms=1200, fade_in_ms=400, fade_out_ms=400)
        return False


def main():
    """Main entry point for Ghost Horror Mode"""
    print("=" * 50)
    print("  👻 GHOST HORROR MODE 👻")
    print("=" * 50)
    
    # Check X11
    if not is_x11():
        print("\n⚠️  Warning: Not running on X11!")
        print("    Keyboard suppression will be disabled.")
        print("    Full Wayland support coming soon.\n")
    
    # Check Ekphos
    launcher = EkphosLauncher()
    ready, message = launcher.check_requirements()
    
    if not ready:
        print(f"\n❌ Error: {message}")
        sys.exit(1)
    
    print(f"✓ {message}")
    print("\nInitializing horror sequence...")
    print("(Press Ctrl+C in terminal to emergency exit)\n")
    
    # Initialize display
    display = Display()
    
    # Initialize input manager
    input_manager = InputManager()
    
    # Setup sound manager (for future use)
    sound = SoundManager()
    
    try:
        # Grab keyboard for intro
        input_manager.grab_keyboard()
        
        # Run intro sequence once at start
        run_intro_sequence(display)
        
        while display.running:
            # Release keyboard for Ekphos
            input_manager.release_keyboard()
            
            # Close display temporarily for Ekphos
            display.close()
            
            # Launch Ekphos
            print("Launching Ekphos...")
            if launcher.launch():
                print("Waiting for Ekphos to exit...")
                launcher.wait_for_exit()
                print("Ekphos closed")
            else:
                print("Failed to launch Ekphos!")
                break
            
            # Re-initialize display for exit sequence
            display = Display()
            # NOTE: Don't grab keyboard here - we need typing for the prompt!
            
            # Run exit sequence (keyboard NOT grabbed so user can type)
            should_exit = run_exit_sequence(display)
            
            if should_exit:
                # User wants to leave
                break
            else:
                # User said no - "Then Return!" was shown, loop back to Ekphos
                print("Returning to Ekphos...")
                # Reset launcher for next iteration
                launcher = EkphosLauncher()
                launcher.check_requirements()
    
    except KeyboardInterrupt:
        print("\n\n🏃 Emergency exit!")
    
    finally:
        # Cleanup
        input_manager.release_keyboard()
        display.close()
        print("\n👋 Exiting Ghost Horror Mode")
        print("Welcome back to the light.\n")


if __name__ == "__main__":
    main()
