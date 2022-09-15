from importlib import import_module

def defaultHook(bot, data):
    ...

def getHook(hook):
    try:
        module = import_module(f".{hook}", __package__)
        return module.hook
    except ModuleNotFoundError:
        return defaultHook