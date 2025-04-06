import os
from typing import Callable

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.livereload import LiveReloadServer

watchedPaths = ["hooks", "overrides"]

def on_serve(server: LiveReloadServer, config: MkDocsConfig, builder: Callable):
    for path in watchedPaths:
        server.watch(path)
    return server