#version 300 es
precision highp float;

in vec3 v_texcoord;

uniform sampler2DArray Texture;

layout (location = 0) out vec4 out_color;

void main() {
    out_color = texture(Texture, v_texcoord);
    out_color = texture(Texture, vec3(1,1,0));
    if (out_color.a < 0.05) {  // why do this?
        // out_color = vec4(1.0, 0.01, 0.5, 1.0);
        discard;
    }
}