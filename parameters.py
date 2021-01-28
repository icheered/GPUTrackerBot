import configargparse


class Parameters:
    def __init__(self):
        self.parser = configargparse.ArgParser(default_config_files=["config.ini"])

        self.init_parameters()

        parameters, unknown = self.parser.parse_known_args()
        self.dictionary = self.create_dict(parameters)

    @staticmethod
    def create_dict(parameters):
        ret = {}
        for option in vars(parameters):
            ret[option] = getattr(parameters, option)
        return ret

    def get_dict(self):
        return self.dictionary

    @staticmethod
    def str2bool(string: str) -> bool:
        """
        Converts a string to a boolean.
        :param string: string to convert to boolean
        :return: True or False
        """
        if string.lower() in ["false", "n", "no", "f"]:
            return False
        elif string.lower() in ["true", "y", "yes", "t"]:
            return True
        else:
            raise TypeError(f"{string} cannot be converted to boolean")

    def init_parameters(self):
        general_group = self.parser.add_argument_group("General")

        general_group.add_argument(
            "--API_KEY",
            type=str,
            help="API key of the bot",
            default="0000000000000000000000000000000",
        )
        general_group.add_argument(
            "--CHAT_ID",
            type=str,
            help="ID of the chat to which the message should be send",
            default="-00000000000000", 
        )
        general_group.add_argument(
            "--GPU",
            type=str,
            help="Which GPU to track3232",
            default="3080",
        )
        general_group.add_argument(
            "--TARGET",
            type=int,
            help="Target price of the GPU",
            default=850, 
        )
        general_group.add_argument(
            "--POLL_INTERVAL",
            type=int,
            help="How often to check for new prices [minutes]",
            default=1, 
        )
        general_group.add_argument(
            "--TARGET_HIT_TIMEOUT",
            type=int,
            help="How long to wait after hitting target price [minutes] (To avoid spam)",
            default=10, 
        )