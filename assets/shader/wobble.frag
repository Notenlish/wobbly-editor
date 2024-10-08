#version 300 es
precision highp float;

in vec2 vertex;
out vec4 out_color;

uniform float time;
uniform float effect_size;
uniform float move_mul;
uniform float some_mul;  // idk how to name this
uniform sampler2D mask_texture;
// uniform sampler2D color_texture;
uniform vec2 screen_size;

// taken from: https://www.shadertoy.com/view/slfGWX
float rand(vec2 co) {
    //Note: fract function return de fractional part of a division and dumps the integer part
    return fract(sin(dot(co.xy, vec2(12.9898f, 78.233f))) * 43758.5453f);
}

vec2 hash(vec2 p) {
    p = vec2(dot(p, vec2(127.1f, 311.7f)), dot(p, vec2(269.5f, 183.3f)));
    //The output must be between 0.0 and 1.0
    return -1.0f + 2.0f * fract(sin(p) * 43758.5453123f);
}

float noise(in vec2 p) {
    const float K1 = 0.366025404f; // (sqrt(3)-1)/2;
    const float K2 = 0.211324865f; // (3-sqrt(3))/6;

    vec2 i = floor(p + (p.x + p.y) * K1);

    vec2 a = p - i + (i.x + i.y) * K2;
    vec2 o = step(a.yx, a.xy);
    vec2 b = a - o + K2;
    vec2 c = a - 1.0f + 2.0f * K2;

    vec3 h = max(0.5f - vec3(dot(a, a), dot(b, b), dot(c, c)), 0.0f);
    vec3 n = h * h * h * h * vec3(dot(a, hash(i + 0.0f)), dot(b, hash(i + o)), dot(c, hash(i + 1.0f)));
    return dot(n, vec3(70.0f));
}

void main() {
    vec2 inp_uv = (vertex * 0.5f + 0.5f);

    // maybe multiply inp_uv with some_mul
    float move_y = (noise(vec2(time, 0.527f) + (inp_uv * some_mul)) - 0.5f) * move_mul;
    float move_x = (noise(vec2(0.843f, time) + (inp_uv * some_mul)) - 0.5f) * move_mul;

    // between 0 and 1 -> make range small so it only moves 1 pixel
    vec2 offset = vec2(move_y, move_x) / screen_size * effect_size;

    // TODO: for the "pixel" effect you need to make the move_y and move_x be "step" based
    // so they should either be -1, 0 or 1.

    vec2 applied_uv = inp_uv + offset;

    vec3 mask_color = texture(mask_texture, applied_uv).rgb;
    // vec3 color_color = texture(color_texture, applied_uv).rgb;

    // float lightness = (mask_color.r + mask_color.g + mask_color.b);
    // vec3 p_color = mask_color * color_color;
    vec3 p_color = mask_color;

    out_color = vec4(p_color, 1.0f);
}