from injector import inject
from pyee import EventEmitter


class LanguageService():
    @inject
    def __init__(self, event_emitter: EventEmitter) -> None:
        self.__event_emitter = event_emitter
        print("Listener registered!")
        self.__event_emitter.on("upload", self.on_upload)

    def on_upload(self, file_name: str):
        print("File: ", file_name)
