from OpenGL.GL import shaders, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER
from OpenGL.arrays import vbo
from numpy import array

vert_shader = '''
        // use a varying value to pass information
        // about color from the vertex to the fragment
        varying vec4 vertex_color;
        void main(){
            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
            vertex_color = gl_Color;
        }
        '''

frag_shader = '''
        varying vec4 vertex_color;
        void main(){
            // interpolates values set into
            // vertex_color from the vertex
            // shader
            gl_FragColor = vertex_color;
        }
        '''


def get_shader():
    vert = shaders.compileShader(vert_shader, GL_VERTEX_SHADER)
    frag = shaders.compileShader(frag_shader, GL_FRAGMENT_SHADER)

    return shaders.compileProgram(vert, frag)
