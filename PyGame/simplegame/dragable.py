# coding: utf-8
# Created by Jabok @ March 28th 2014
from .mouselistener import MouseListener
class Dragable(MouseListener):
    """This mix-in should be used with an object that has a Transform
    field named 'transform'. Otherwise the rect will be used."""
    def __init__(self):
        super().__init__() # Initialize the mouse listener
    
    def on_drag(self, pos, rel, button):
        if hasattr(self, "transform"):
            self.transform.pos += rel
        elif hasattr(self, "rect"):
            self.rect = self.rect.move(rel) # Might be less precise
        else:
            errmsg = """Unknown object. Please add a 'rect' or 'transform'
            member to the object before making it dragable :)."""
            raise Exception(errmsg)