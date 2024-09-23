#version 330 core

uniform vec4 preview_rect;

vec2 vertices[4] = vec2[](
    // top left
vec2(-1.0, -1.0),
    // top right
vec2(-1.0, 1.0),
    // bottom left
vec2(1.0, -1.0),
    // bottom right
vec2(1.0, 1.0));

out vec2 vertex;

void main() {
    gl_Position = vec4(vertices[gl_VertexID], preview_rect.x * 0.0000000000001, 1.0);
    vertex = vertices[gl_VertexID];
}