import string

import pygame as pg

ACCEPTED = string.ascii_letters + string.digits + string.punctuation + " "


class TextBox(object):
    def __init__(self, rect, **kwargs):
        self.rect = pg.Rect(rect)
        self.buffer = []
        self.text = None
        self.rendered = None
        self.render_rect = None
        self.render_area = None
        self.blink = True
        self.blink_timer = 0.0
        self.process_kwargs(kwargs)
        self.buffer = list(str(self.default))

    def process_kwargs(self, kwargs):
        defaults = {
            "id": None,
            "function": None,
            "color": pg.Color("white"),
            "font_color": pg.Color("black"),
            "border_color": pg.Color("grey"),
            "outline_width": 2,
            "active_color": pg.Color("blue"),
            "font": pg.font.Font(None, self.rect.height + 4),
            "clear_on_enter": False,
            "inactive_on_enter": False,
            "active": True,
            "default": "",
        }
        for kwarg in kwargs:
            if kwarg in defaults:
                defaults[kwarg] = kwargs[kwarg]
            else:
                raise KeyError(
                    "{} accepts no keyword {}.".format(self.__class__.__name__, kwarg)
                )
        self.__dict__.update(defaults)

    def check_event(self, event):
        if event.type == pg.KEYDOWN and self.active:
            if event.key in (pg.K_RETURN, pg.K_KP_ENTER):
                self.execute()
            elif event.key == pg.K_BACKSPACE:
                if self.buffer:
                    self.buffer.pop()
            elif event.unicode in ACCEPTED:
                self.buffer.append(event.unicode)
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)

    def execute(self):
        if self.function:
            self.function()
            # self.command(self.id,self.text)
        self.active = not self.inactive_on_enter
        if self.clear_on_enter:
            self.buffer = []

    def update(self):
        new = "".join(self.buffer)
        if new != self.text:
            self.text = new
            self.rendered = self.font.render(self.text, True, self.font_color)
            self.render_rect = self.rendered.get_rect(
                x=self.rect.x + 2, centery=self.rect.centery
            )
            if self.render_rect.width > self.rect.width - 6:
                offset = self.render_rect.width - (self.rect.width - 6)
                self.render_area = pg.Rect(
                    offset, 0, self.rect.width - 6, self.render_rect.height
                )
            else:
                self.render_area = self.rendered.get_rect(topleft=(0, 0))
        if pg.time.get_ticks() - self.blink_timer > 500:
            self.blink = not self.blink
            self.blink_timer = pg.time.get_ticks()

    def render(self, surface):
        # outline_color = self.active_color if self.active else self.outline_color
        outline = self.rect.inflate(self.outline_width * 2, self.outline_width * 2)
        surface.fill(self.border_color, outline)
        surface.fill(self.color, self.rect)
        if self.rendered:
            surface.blit(self.rendered, self.render_rect, self.render_area)
        if self.blink and self.active:
            curse = self.render_area.copy()
            curse.topleft = self.render_rect.topleft
            surface.fill(self.font_color, (curse.right + 1, curse.y, 2, curse.h))


if __name__ == "__main__":

    class Control:
        def __init__(self):
            pg.init()
            self.screen = pg.display.set_mode((800, 600))
            self.done = False
            self.clock = pg.time.Clock()

            config = {"clear_on_enter": True}
            self.textbox = TextBox((10, 10, 100, 25), function=self.test, **config)

        def test(self):
            print(self.textbox.final)

        def events(self):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.done = True
                self.textbox.check_event(event)

        def update(self):
            self.textbox.update()

        def render(self):
            self.textbox.render(self.screen)

        def run(self):
            while not self.done:
                self.events()
                self.update()
                self.render()
                pg.display.update()
                self.clock.tick(60)

    app = Control()
    app.run()
