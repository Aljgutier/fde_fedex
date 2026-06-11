# 5 - Tools and Custom Agent


Agents with Tools

Out of the box, AI agents can only generate text. To interact with the real world—look up data, perform calculations, call APIs, query databases—agents need tools.

Framework with tools

* Features for tool integration:
* @agent.tool decorator for registration
* Automatic function signature analysis
* Type annotations become tool schemas
* Docstrings become tool descriptions
* Support for sync and async tools


Tool Design Principles

* Single responsibility—one tool, one task
* Clear, descriptive names and parameters
* Robust error handling
* Type-safe inputs and outputs


Scenario
* You’re building a customer service agent for an e-commerce company. The agent needs to:
* Look up customer order status
* Calculate shipping costs
* Check product availability
* Process refund requests

Problem Statement

* Objective: Build a customer service agent that integrates custom tools for order status lookup, inventory checking, and shipping calculation, enabling the agent to provide accurate real-time information.

* Expected Outcome: A working agent with **three** registered tools that correctly selects the appropriate tool for each query, handles error conditions gracefully, and includes instrumentation for tracking tool usage analytics.