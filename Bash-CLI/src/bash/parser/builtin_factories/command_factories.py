from .cat_factory import CatFactory
from .echo_factory import EchoFactory
from .pwd_factory import PwdFactory
from .wc_factory import WcFactory

COMMAND_FACTORIES = {"cat": CatFactory(),
                     "echo": EchoFactory(),
                     "pwd": PwdFactory(),
                     "wc": WcFactory()
                     }
