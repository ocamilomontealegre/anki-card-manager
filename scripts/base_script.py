from abc import ABC, abstractmethod


class Script(ABC):
    @abstractmethod
    def execute(self):
        """
        Executes an script
        """
        pass