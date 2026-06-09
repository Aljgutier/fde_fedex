Had to to the following to get tests to work on PC

put the following in a file
```text
{"test":"lab task"}
```

```sh`      
curl.exe -X POST "http://localhost:5000/tasks" \
      -H "Content-Type: application/json" \
      --data-binary "@payload.json"
```

use curl.exe
```
 curl.exe http://localhost:5000/tasks
[
  {
    "id": 1,
    "status": "pending",
    "title": "lab task"
  }
]
```

curl.exe http://localhost:5000/tasks?status=pending