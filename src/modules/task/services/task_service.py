from injector import inject


class TaskService:
    @inject
    def __init__(self) -> None:
        pass
    
    def get_task(self, id: str) -> str:
        pass
