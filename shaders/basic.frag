#version 330

in vec3 v_color;  // Color que viene desde el Vertex Shader
out vec4 f_color;

void main() {
    f_color = vec4(v_color, 1.0); // Se usa el color directamente
}
