from abc import ABC, abstractmethod

class IAppController(ABC):
    @abstractmethod
    def run_import(self):
        pass

    @abstractmethod
    def show_stats(self):
        pass
