# 7 Dependency Management

Production agents need access to external resources—databases, APIs, caches, configuration. Hardcoding these creates tight coupling, makes testing difficult, and causes resource leaks.

Dependency injection solves these problems:


Framework

Dependency Injection (DI)
* Pass dependencies to components rather than hardcoding
* Enables testing, flexibility, and proper resource management

RunContext

* Pydantic AI’s DI mechanism
* Provides dependencies to tools and system prompts
* Type-safe dependency passing via deps_type

State Isolation

* Each agent run gets independent context
* No shared mutable state between runs
* Thread-safe concurrent execution


Scenario
* order management agent that needs:
* Database access - Query orders, customers, inventory
* Cache layer - Reduce database load
* Email service - Send notifications
* Configuration - API keys, timeouts, feature flagsr
* Logger - Structured logging

Problem Statement
* Objective: Build an order management agent that uses Pydantic AI’s RunContext to inject a database, cache, email service, and configuration, demonstrating proper resource management and state isolation between concurrent runs.

* Expected Outcome: A working agent with tools that transparently access injected dependencies, a dependency factory that manages resource lifecycle, and a pytest suite that passes using mocked dependencies to verify cache-hit, cache-miss, and isolation behavior.