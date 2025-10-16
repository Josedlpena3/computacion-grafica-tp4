import moderngl
import pyglet

class Window(pyglet.window.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)
        self.ctx = moderngl.create_context(require=410)
        self.scene = None

    def set_scene(self, scene):
        self.scene = scene
        scene.start()  

    def on_draw(self):
        self.clear()
        self.ctx.clear(0.05, 0.06, 0.08, 1.0)
        self.ctx.enable(moderngl.DEPTH_TEST) # detecta que esta adelante y que esta atras 

        if self.scene:
            self.scene.render()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.scene is None:
            return

        # Convertir posición del mouse a coordenadas normalizadas (u, v)
        u = x / self.width
        v = y / self.height

        self.scene.on_mouse_click(u, v)

    def on_resize(self, width, height):
        if self.scene:
            self.scene.on_resize(width, height)

    def run(self):
        pyglet.app.run()
