from ConfigParser import ConfigParser

from aw_core import config

default_client_config = ConfigParser()
default_client_config.add_section('server')
default_client_config.set("server", "hostname", "localhost")
default_client_config.set("server", "port", "5600")
# default_client_config["server"] = {
#     "hostname": "localhost",
#     "port": "5600",
# }
default_client_config.add_section('server-testing')
default_client_config.set("server-testing", "hostname", "localhost")
default_client_config.set("server-testing", "port", "5666")
# default_client_config["server-testing"] = {
#     "hostname": "localhost",
#     "port": "5666"
# }


def load_config():
    return config.load_config("aw-client", default_client_config)
