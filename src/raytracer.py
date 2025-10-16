from texture import Texture
from shader_program import ComputeShaderProgram
from bvh import BVH
import numpy as np
import glm

class RayTracer:
    def __init__(self, camera, width, height):
        self.camera = camera
        self.width = width
        self.height = height
        self.framebuffer = Texture(width=width, height=height, channels_amount=3)
        self.camera.set_sky_colors(top=(16, 150, 222), bottom=(181, 224, 247))  # gradiente de cielo por default

    def trace_ray(self, ray, objects):
        for obj in objects:
            if obj.check_hit(ray.origin, ray.direction):
                return (255, 0, 0)  # rojo
        height = ray.direction.y
        return self.camera.get_sky_gradient(height)

    def render_frame(self, objects):
        for y in range(self.height):
            for x in range(self.width):
                u = x / (self.width - 1)
                v = y / (self.height - 1)
                ray = self.camera.raycast(u, v)
                color = self.trace_ray(ray, objects)
                self.framebuffer.set_pixel(x, y, color)

    def get_texture(self):
        return self.framebuffer.image_data

class RayTracerGPU:
    def __init__(self, ctx, camera, width, height, output_graphics):
        self.ctx = ctx
        self.camera = camera
        self.width = width
        self.height = height
        self.compute_shader = ComputeShaderProgram(self.ctx, "../shaders/raytracing.comp")
        self.output_graphics = output_graphics

        self.texture_unit = 0
        self.output_texture = Texture("u_texture", self.width, self.height, 4, None, (255, 255, 255, 255))
        self.output_graphics.update_texture("u_texture", self.output_texture.image_data)
        self.output_graphics.bind_to_image("u_texture", self.texture_unit, read=False, write=True)

        self.compute_shader.set_uniform('cameraPosition', self.camera.position)        
        self.compute_shader.set_uniform('inverseViewMatrix', self.camera.get_inverse_view_matrix())
        self.compute_shader.set_uniform('fieldOfView', self.camera.fov)

    def resize(self, width, height):
        self.width, self.height = width, height
        self.output_texture = Texture("u_texture", width, height, 4, None, (255, 255, 255, 255))
        self.output_graphics.update_texture("u_texture", self.output_texture.image_data)

    def matrix_to_ssbo(self, matrix, binding = 0):
        buffer = self.ctx.buffer(matrix.tobytes())
        buffer.bind_to_storage_buffer(binding=binding) # tiene que ser igual al computer shader

    def primitives_to_ssbo(self, primitives, binding = 3):
        self.bvh_nodes = BVH(primitives)
        self.bvh_ssbo = self.bvh_nodes.pack_to_bytes()
        buf_bvh = self.ctx.buffer(self.bvh_ssbo)
        buf_bvh.bind_to_storage_buffer(binding=binding)


    def run(self):
        groups_x = (self.width + 15) // 16
        groups_y = (self.height + 15) // 16

        self.compute_shader.run(groups_x=groups_x, groups_y=groups_y, groups_z=1)
        self.ctx.clear(0.0, 0.0, 0.0, 1.0)
        self.output_graphics.render({"u_texture": self.texture_unit})





