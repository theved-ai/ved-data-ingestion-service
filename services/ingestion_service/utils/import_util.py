import importlib
import logging
import pkgutil

logger = logging.getLogger(__name__)

def load_package(package_name: str):
    package = importlib.import_module(package_name)
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        if not is_pkg:
            logger.debug(f"Importing tool module: {name}")
            importlib.import_module(name)