


class ProtocolFactory:
    """Factory for creating needed protocols."""
    _reg = {}

    @classmethod
    def reg(cls, protocol_name: str, mode: str, type: str):
        def decorator(command_class):
            cls._reg[name] = command_class
            return command_class
        return decorator