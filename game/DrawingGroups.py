from pyglet.gl import GL_TEXTURE_2D, glEnable, glDisable, glBindTexture
from pyglet.graphics import Group

class TextureEnableGroup(Group):
    def set_state(self):
        glEnable(GL_TEXTURE_2D)

    def unset_state(self):
        glDisable(GL_TEXTURE_2D)

texture_enable_group = TextureEnableGroup()


class TextureBindGroup(Group):
    def __init__(self, texture):
        super(TextureBindGroup, self).__init__(parent=texture_enable_group)
        assert texture.target == GL_TEXTURE_2D
        self.texture = texture

    def set_state(self):
        glBindTexture(GL_TEXTURE_2D, self.texture.id)

    # No unset_state method required.

    def __eq__(self, other):
        return (self.__class__ is other.__class__ and
                self.texture == other.__class__) # FIXME?  == other.texture
