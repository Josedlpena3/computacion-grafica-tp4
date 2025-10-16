from moderngl import Attribute, Uniform
import glm

class ShaderProgram:
    def __init__(self, ctx, vertex_shader_path, fragment_shader_path):
        with open(vertex_shader_path) as file:
            vertex_shader = file.read()
        with open(fragment_shader_path) as file:
            fragment_shader = file.read()
        self.prog = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        attributes = []
        uniforms = []
        for name in self.prog:
            member = self.prog[name]
            if type(member) is Attribute:
                attributes.append(name)
            if type(member) is Uniform:
                uniforms.append(name)

        self.attributes = list(attributes)
        self.uniforms = uniforms

    def set_uniform(self, name, value):
        if name in self.uniforms:
            uniform = self.prog[name]
            if isinstance(value, glm.mat4):
                uniform.write(value.to_bytes())
            elif hasattr(uniform, "value"):
                uniform.value = value

class ComputeShaderProgram:
    def __init__(self, ctx, compute_shader_path):
        with open(compute_shader_path) as file:
            compute_source = file.read()
        self.prog = ctx.compute_shader(compute_source)

        uniforms = []
        for name in self.prog:
            member = self.prog[name]
            if type(member) is Uniform:
                uniforms.append(name)
        self.uniforms = uniforms

    def set_uniform(self, name, value):
        if name in self.uniforms:
            uniform = self.prog[name]
            if isinstance(value, glm.mat4):
                uniform.write(value.to_bytes())
            elif hasattr(uniform, "value"):
                uniform.value = value

    def run(self, groups_x, groups_y, groups_z=1):
        self.prog.run(group_x=groups_x, group_y=groups_y, group_z=groups_z)

