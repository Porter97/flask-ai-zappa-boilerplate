class Executor:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if not Executor.__instance:
            Executor()
        return Executor.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Executor.__instance:
            raise Exception("This class is a singleton!")
        else:
            Executor.__instance = self

    @staticmethod
    def execute_write(command):
        return command.execute()

    @staticmethod
    def execute_read(command):
        return command.execute()
