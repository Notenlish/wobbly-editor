#version 330 core
// These need to be rewritte

uniform sampler2D Texture;

in vec2 vertex;
out vec4 out_color;

void main() {
    vec2 inp_uv = (vertex * 0.5 + 0.5);

    vec3 inp_color = texture(Texture, inp_uv).rgb;
    inp_color.rg = vec2(0.0);
    inp_color.r = inp_uv.x;
    inp_color.g = inp_uv.y;
    out_color = vec4(inp_color, 1.0);
}