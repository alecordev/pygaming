from . import control


def main():
    app = control.Control(fullscreen=False)
    app.run()
