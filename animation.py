#!/usr/bin/env python3

import pyglet, time
from . import dispatcher

"""
Check http://cwru-hackers.googlecode.com/svn-history/r233/splatterboard/trunk/draw.py

"""

MAX_OBJECTS = 20

class Context(dispatcher.Dispatcher):

    def __init__(self, width=800, height=600, background=(1.0, 1.0, 1.0, 1.0), fullscreen=False, title="animation", chrome=True, screen=0, smooth=True):
        self._width = width
        self._height = height
        self._fps = 60.0
        self._background = background
        self._fullscreen = fullscreen
        self._title = title
        self._screen = screen
        self._chrome = chrome
        self.window = None        
        self.last_frame = 0
        self.smooth = smooth
        self.objects = []
        dispatcher.Dispatcher.__init__(self)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def fps(self):
        return self._fps

    def start(self, draw_func):
        config = pyglet.gl.Config(sample_buffers=1, samples=4, depth_size=24, double_buffer=True)
        style = pyglet.window.Window.WINDOW_STYLE_DEFAULT if self._chrome else pyglet.window.Window.WINDOW_STYLE_BORDERLESS
        screens = pyglet.window.get_platform().get_default_display().get_screens()
        screen_index = min(self._screen, len(screens) - 1)
        screen = screens[screen_index]
        if not (self._fullscreen and screen_index !=0):
            self.window = pyglet.window.Window(config=config, width=self.width, height=self.height, resizable=False, fullscreen=self._fullscreen, caption=self._title, style=style, screen=screen)
        else:   # hack because pyglet fullscreen doesnt work on secondary screen
            self._width = screen.width
            self._height = screen.height
            self.window = pyglet.window.Window(config=config, width=self.width, height=self.height, resizable=False, fullscreen=False, caption=self._title, style=style, screen=screen)
            self.window.set_location(screen.x, screen.y)
        self.window.on_mouse_press = self.on_mouse_press
        self.window.on_mouse_release = self.on_mouse_release
        self.draw_func = draw_func
        pyglet.gl.glClearColor(*self._background)
        if self.smooth:
            pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)                             
            pyglet.gl.glEnable(pyglet.gl.GL_BLEND)                                                            
            pyglet.gl.glEnable(pyglet.gl.GL_LINE_SMOOTH)
            pyglet.gl.glHint(pyglet.gl.GL_LINE_SMOOTH_HINT, pyglet.gl.GL_NICEST)    
        self.window.on_draw = self.draw_loop
        pyglet.clock.schedule_interval(lambda x: x, 1.0 / 120.0)
        pyglet.app.run()            

    def draw_loop(self):
        self.window.clear()
        self.draw_func()
        for o in self.objects:
            o.draw()
        t = time.time()
        elapsed = t - self.last_frame
        if 1.0 / elapsed < 30.0:
            print(("%f fps" % (1.0 / elapsed)))
        self.last_frame = t

    def line(self, x1, y1, x2, y2, color=(0., 0., 0., 1.), thickness=1.0):
        pyglet.gl.glColor4f(*color)    
        pyglet.gl.glLineWidth(thickness) 
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
            ('v2f', (x1 * self.width, y1 * self.height, x2 * self.width, y2 * self.height))
        )        

    def lines(self, points, color=(0., 0., 0., 1.), thickness=1.0):
        pyglet.gl.glColor4f(*color)    
        pyglet.gl.glLineWidth(thickness) 
        points = [(item * self.width) if (i % 2 == 0) else (item * self.height) for sublist in points for (i, item) in enumerate(sublist)] # flatten
        pyglet.graphics.draw(len(points) // 2, pyglet.gl.GL_LINE_STRIP, ('v2f', points))        

    def plot(self, signal, color=(0., 0., 0., 1.), thickness=1.0):
        points = [(float(s) / self.width, sample) for (s, sample) in enumerate(signal)]
        self.lines(points, color=color, thickness=thickness)    

    def rect(self, x, y, width, height, color=(0., 0., 0., 1.), thickness=1.0):
        pyglet.gl.glColor4f(*color)    
        pyglet.gl.glLineWidth(thickness) 
        x *= self.width
        y *= self.height
        width *= self.width
        height *= self.height
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
            ('v2f', (x, y, x, y + height, x + width, y + height, x + width, y)),
            # ('c3b', (color, color, color, color))
        )

    def arc():
        pass

    def curve():
        pass

    def label(self, x, y, text="", font="Helvetica", size=36, width=400, color=(0., 0., 0., 1.), center=False):
        # why is the antialiasing so awful
        color = [int(c * 255) for c in color] # why?
        l = pyglet.text.HTMLLabel(text, x=x * self.width, y=y * self.height, width=width, multiline=True)
        l.font_name = font
        l.font_size = size
        l.color = color
        if center:
            l.anchor_x = 'center'
        self.objects.append(l)
        l.draw()
        return l

    def on_mouse_press(self, x, y, button, modifiers):
        self.fire('mouse_press', (x/self.width, y/self.width, button, modifiers))

    def on_mouse_release(self, x, y, button, modifiers):
        self.fire('mouse_release', (x/self.width, y/self.width, button, modifiers))


def rgb_to_html(rgb_tuple):
    return '#%02x%02x%02x' % rgb_tuple[:3]


if __name__ == "__main__":

    from random import random

    ctx = Context(1200, 600, background=(0.9, 0.9, 0.9, 1.), fullscreen=False)    

    def draw():
        ctx.line(random(), random(), random(), random(), thickness=2.0)#, color=(1., 1., 1., 1.))    

    ctx.start(draw)

