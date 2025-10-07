"""
Properties module - Gestão de propriedades
"""

from .models import Property
from .schemas import PropertyCreate, PropertyUpdate, PropertyResponse
from .repository import PropertyRepository
from .controller import property_controller
from .router import router

__all__ = [
    "Property",
    "PropertyCreate", 
    "PropertyUpdate",
    "PropertyResponse",
    "property_repository",
    "property_controller",
    "router"
]