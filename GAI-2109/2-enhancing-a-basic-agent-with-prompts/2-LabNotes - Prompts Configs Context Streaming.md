# 2-LabNotes Enhancing Basic Agent with Prompts and Configurations

In this lab, you’ll transform a basic agent into a production-ready assistant by:
* Crafting detailed system prompts with clear instructions
* Experimenting with model parameters to optimize behavior
* Comparing different model capabilities
* Implementing advanced features like streaming

Configurations
* temperature - Controls randomness (0.0 = deterministic, 2.0 = very creative)
* max_tokens - Limits response length
* top_p - Nucleus sampling for diversity
* Model selection across providers

Scenarioo
* Generate blog post outlines with specific formatting
* Maintain a consistent brand voice (professional but approachable)
* Adapt its verbosity based on the task (concise summaries vs. detailed articles)
* Provide real-time feedback as it generates content


# implemented three exercices
* enhanced_agent.py
* challenge1.py - dynamic context
* challenge2.py - streaming output