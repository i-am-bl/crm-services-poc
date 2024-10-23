from enum import Enum

from . import constants as cnst


class ItemAdjustmentType(str, Enum):
    DOLLAR = cnst.DOLLAR
    PERCENTAGE = cnst.PERCENTAGE


class EntityTypes(str, Enum):
    ENTITY_INDIVIDUAL = cnst.ENTITY_INDIVIDUAL
    ENTITY_NON_INDIVIDUAL = cnst.ENTITY_NON_INDIVIDUAL
