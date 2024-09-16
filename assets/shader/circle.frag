#version 300 es
precision highp float;

in vec3 v_texcoord;

uniform sampler2DArray Texture;

layout (location = 0) out vec4 out_color;

void main() {
    out_color = texture(Texture, v_texcoord);
    if (out_color.a < 0.05) {  // why do this?
        discard;
    }
}