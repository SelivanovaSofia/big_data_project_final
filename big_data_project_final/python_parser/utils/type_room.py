from enum import Enum
from enum import IntEnum

class TypeRoom(IntEnum):
    ONE_ROOM = 1  # Flatrent and flatsale
    TWOO_ROOM = 2  # Flatrent and flatsale
    THREE_ROOM = 3  # Flatrent and flatsale
    STUDIO = 9  # Flatrent and flatsale
    ROOM_IN_APARTMENT = 0  # Flatrent and flatsale
    FREE_PLAN = 7  # only sale