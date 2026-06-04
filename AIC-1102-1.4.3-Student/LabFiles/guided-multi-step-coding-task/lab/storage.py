from itertools import count


class TaskStore:
    def __init__(self):
        self._tasks = {}
        self._ids = count(1)

    def create(self, title, status="pending"):
        task_id = next(self._ids)
        task = {"id": task_id, "title": title, "status": status}
        self._tasks[task_id] = task
        return task

    def list_all(self):
        return list(self._tasks.values())
