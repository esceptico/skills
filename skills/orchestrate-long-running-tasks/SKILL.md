---
name: orchestrate-long-running-tasks
description: Orchestrate explicitly requested long-running work across Codex tasks, using Astra for coordination and Sol or Luna for execution, with verification and a 15-minute heartbeat. Use when the user asks to delegate, parallelize, or supervise substantial work across tasks.
metadata:
  version: "1.0.0"
---

# Orchestrate Long-Running Tasks

Use GPT-6 Astra as the coordinator. Keep the coordinator focused on decomposition, task ownership, evidence review, dependency management, and final synthesis.

## Dispatch

Only create separate Codex tasks when the user explicitly requests delegation, parallel work, or this orchestration workflow.

1. Split the goal into independent, bounded assignments with clear inputs, outputs, constraints, and verification criteria. Avoid overlapping ownership.
2. Use GPT-5.6 Sol for substantial implementation, investigation, or judgment-heavy work. Use GPT-5.6 Luna for cheap, well-specified, mechanical work. Keep uncertain architecture and cross-task decisions with Astra.
3. Create each task with a complete standalone prompt. Include the relevant project, starting state, allowed scope, expected artifact, and how to prove completion.
4. After dispatch, wait for initial progress. Record task IDs and dependencies. Do not duplicate work in the coordinator unless a worker is blocked or its result needs independent verification.

## Supervise

After workers are running, create one heartbeat attached to the coordinating task that runs every 15 minutes. Reuse an existing matching heartbeat instead of creating a duplicate.

The heartbeat should:

- inspect each worker's latest status with compact task-status tools;
- compare progress with the assignment and verification criteria;
- send a concise correction only when a worker is blocked, drifting, duplicating work, or missing evidence;
- surface approvals or user decisions without answering them on the user's behalf;
- stay quiet when nothing meaningful changed;
- notify the user only for a meaningful change, completion, failure, or required action;
- stop or disable itself after all work is complete and the coordinator has synthesized the result.

Use task messaging for course corrections. Preserve each worker's current model unless a model change is part of the correction.

## Finish

Review worker outputs against their stated evidence, resolve conflicts, and run proportionate integration checks. Report one synthesized outcome, not a transcript of worker activity. Distinguish verified results from unresolved assumptions, then disable the heartbeat.
