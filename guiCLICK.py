from pynput import mouse, keyboard
import time

# Function to perform a mouse click
def perform_click(x_pos, y_pos):
    with mouse.Controller() as mouse_controller:
        mouse_controller.position = (x_pos, y_pos)
        time.sleep(0.1)
        mouse_controller.click(mouse.Button.left, 3)


# Function to handle key presses
def on_key_press(key):
    try:
        print("Pressed: {}", key)
        if key.char == '¶':
            perform_click(444, 222)
        elif key.char == '•':
            perform_click(940, 222)
        elif key.char == 'ª':
            perform_click(1440, 222)
        elif key.char == 'º':
            perform_click(1930, 222)
        elif key.char == '¡':
            perform_click(43, 314)
        elif key.char == '™':
            perform_click(590, 314)
        elif key.char == '£':
            perform_click(1080, 314)
        elif key.char == '¢':
            perform_click(1558, 314)

    except AttributeError:
        print("Errror while pressing: {}", key)
        pass


# Start listening for key presses
keyboard_listener = keyboard.Listener(on_press=on_key_press)
keyboard_listener.start()

# Keep the script running
keyboard_listener.join()
