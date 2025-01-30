"""
This package encapsulates multiple containers for globally managing dependency injections.

The containers in this package handle the management and injection of dependencies
across various modules, providing a central place to access shared services and components.
"""

from .auth import container as auth_container
from .database import container as database_container
from .orchestrators import container as orchs_container
from .services import container as services_container
from .statements import container as statements_container
