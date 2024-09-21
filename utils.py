def load_shader_file(filepath: str):
    with open(filepath, "r") as f:
        data = f.read()
    return data


def load_vertex_shader(name: str):
    return load_shader_file(f"assets/shader/{name}.vert")


def load_frag_shader(name: str):
    return load_shader_file(f"assets/shader/{name}.frag")
