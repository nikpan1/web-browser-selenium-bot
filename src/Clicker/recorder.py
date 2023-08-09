from pynput.mouse import Listener

def click(x,y,button,pressed):
    print("Mouse is Clicked at (",x,",",y,")","with",button)
    return (x, y)
