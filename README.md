# Daily Standup Generator

A simple automation tool that generates a daily standup update based on Git commit history, scheduled time windows, and simulated task sources.

## Problem

Writing daily standup updates manually is repetitive, time-consuming, and easy to miss completed tasks, especially when work is spread across commits and multiple tools.

## Solution

This project automates the core logic of daily standup preparation by:

- Using Git commit history as a reliable source of completed work
- Generating standup reports based on a configurable time window (scheduling support)
- Simulating integration with task management tools (e.g. Jira / Microsoft Teams)
- Providing a lightweight AI-style summarization layer to group and clean raw data

The result is a consistent, repeatable standup report generated with a single command.

## Features

### 1. Git-based activity tracking
- Collects Git commit messages within a configurable time window
- Ensures completed work is always captured from actual development activity

### 2. Scheduling support (time-based standup)
- Standup generation is based on a time window instead of a fixed commit count
- Default demo configuration uses a **10-minute window** for fast testing
- Can be easily adjusted to **24 hours** for real daily usage

### 3. Simulated task integration (Jira / Microsoft Teams)
- Tasks are loaded from a local `tasks.json` file
- This simulates pulling tasks from external systems without requiring real API access
- Allows combining Git activity with planned or assigned work

### 4. AI-style summarization (mock)
- Commit messages and tasks are grouped and cleaned into a readable standup format
- This layer is designed as a placeholder for real AI-based summarization in the future
- Demonstrates how AI can be plugged into the workflow without overengineering

## How to run

```bash
python standup.py
```

## Reflection

- This project focuses on automating the most repetitive part of the daily standup process by relying on real developer activity instead of manual reporting.
- By combining time-based scheduling, task simulation, and an AI-ready summarization layer, the solution demonstrates how a simple automation script can evolve into a scalable workflow tool.
- The design intentionally favors clarity and extensibility over full production integrations, making it suitable as a foundation for further development.

## Short Demo
https://drive.google.com/file/d/1uWm47XbvjDcV0uCoP4DPftLeLiRHIFcG/view?usp=sharing