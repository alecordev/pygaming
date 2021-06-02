from . import control


def main(fullscreen=False):
    app = control.Control(fullscreen)
    app.run()
