class LightStateManager(object):

    def __init__(self, light_length: int, identifier=0):
        self._identifier = identifier
        self._light_array = [(0,0,0)]*light_length
        self._light_length = light_length

    @property
    def ident(self):
        return self._identifier

    @property
    def length(self):
        return self._light_length

    @property
    def lights(self):
        return self._light_array

    def update_light(self, index, r, g, b):
        new_tuple = (r, g, b)
        self._light_array[index] = new_tuple

    def display(self):
        print("LIGHT:", self._light_array)
    