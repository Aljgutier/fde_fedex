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

    def list_all(self, status=None):
        if status is None:
            return list(self._tasks.values())
        return [task for task in self._tasks.values() if task["status"] == status]

    def get(self, task_id):
        return self._tasks.get(task_id)

    def update(self, task_id, fields):
        task = self._tasks.get(task_id)
        if task is None:
            return None
        task.update(fields)
        return task

    def delete(self, task_id):
        if task_id not in self._tasks:
            return False
        del self._tasks[task_id]
        return True
