import importlib
import logging

from logtron.config import discover_config as discover_config_base
from logtron.formatters import JsonFormatter
from logtron.util import flatten_dict, merge

is_configured = False


def __get_handlers(config, formatter):
    config = {k.lower(): v for k, v in config.items()}

    handlers = [(i,) + tuple(i.rsplit(".", 1)) for i in config["handlers"]]
    classes = [i[2] for i in handlers]

    for handler, module_name, class_name in handlers:
        HandlerClass = getattr(importlib.import_module(module_name), class_name)
        instance = None
        args = {}
        if config.get(handler.lower()) is not None:
            merge(args, config[handler.lower()])
        if classes.count(class_name) == 1 and config.get(class_name.lower()) is not None:
            merge(args, config[class_name.lower()])
        instance = HandlerClass(**args)
        instance.setFormatter(formatter)
        yield instance


def autodiscover(name=None, level=logging.INFO, **kwargs):
    global is_configured

    refresh = kwargs.get("refresh", False)
    if not refresh and is_configured:
        return logging.getLogger(name)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    while len(logger.handlers) > 0:
        logger.removeHandler(logger.handlers[0])

    discover_config = kwargs.get("discover_config", discover_config_base)
    config = discover_config(kwargs.get("config"))

    context = config.get("context", {})
    formatter = JsonFormatter(
        discover_context=kwargs.get("discover_context", lambda: context),
        flatten=kwargs.get("flatten", False),
    )
    handlers = __get_handlers(config, formatter)
    for i in handlers:
        logger.addHandler(i)

    is_configured = True

    return logger
