# Import everything into the same namespace
from .game import *
from .mixins import *
from .objects import *
from .transform import *
from .vector import *
from .mouselistener import *
from .drawutils import *
from .dragable import *
from .gui import *
from .group import *
from .jukebox import Jukebox
from .animation import Animation
from .sprite import Sprite
from .loader import Loader

# Clean the namespace again :)
del game
del mixins
del objects
del transform
del vector
del mouselistener
del drawutils
del dragable
del group
del jukebox
del animation
del sprite
del loader
# gui # Keep gui in the namespace for finding the relevant classes :)

del pygame
del math