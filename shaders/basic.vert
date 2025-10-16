#version 330

in vec3 in_pos;
in vec3 in_color;

out vec3 v_color;

uniform mat4 Mvp;

void main() {
    v_color = in_color;
    gl_Position = Mvp * vec4(in_pos, 1.0);
}
