
Without proper lifecycle management:

* Resource leaks accumulate over time
* Connections remain open unnecessarily
* Configuration errors surface late
* Testing becomes difficult
* Deployments fail unpredictably

Life Cycle Stages

Initialization
```
Load config → Validate → Initialize connections → Ready
```

Runtime
```
Request → Get/Create resources → Execute → Release → Repeat
```

Shutdown

```
Flush caches → Close connections → Save state → Exit
```


Scenario
* You’re building a production agent service that uses:
* PostgreSQL - Customer and order data (connection pool)
* Redis - Response caching (persistent connection)
* HTTP client - External API calls (connection pooling)
* S3 bucket - Document storage (client with credentials)
* Configuration - Environment-based settings

All resources must:
* Initialize cleanly on startup
* Be reused efficiently during runtime
* Clean up properly on shutdown
* Handle failures gracefully


Problem Statement
* Objective: Build a production agent service with full dependency lifecycle management, using Pydantic Settings for type-safe configuration, context managers for automatic resource cleanup, and a LifecycleManager that initializes and shuts down all dependencies in correct dependency order.

* Expected Outcome: A working service that initializes PostgreSQL, Redis, and HTTP client connections on startup, uses them in agent tools, cleans them up reliably on shutdown even during failures, and integrates cleanly with FastAPI’s lifespan hook and a pytest suite using fake dependencies.