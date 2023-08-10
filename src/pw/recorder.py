from pynput.mouse import Controller, Listener, Button

def wait_for_mouse_click():
    global cords
    cords = [0,0]
    def on_click(x, y, button, pressed):
        if pressed and button == Button.left:
            cords[0] = x
            cords[1] = y
            # Stop listening for mouse events
            listener.stop()

    # Create a listener for mouse events
    with Listener(on_click=on_click) as listener:
        listener.join()
    
    return cords 

def press_pos(x, y):
    mouse = Controller()

    mouse.position = (x, y)
    mouse.click(Button.left)

