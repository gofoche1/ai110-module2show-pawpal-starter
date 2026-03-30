# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling Features

The scheduler now includes several intelligent algorithmic improvements:

- Time-based sorting: Tasks are sorted chronologically by scheduled time (HH:MM format) to present a clear, ordered daily plan.
- Task filtering: Filter tasks by completion status (pending/completed) and/or pet name for flexible reporting and management.
- Recurring task automation: When a daily or weekly task is marked complete, the scheduler automatically generates the next occurrence with an updated due date using Python's `timedelta`.
- Conflict detection: The scheduler detects and warns about tasks scheduled at the same time, preventing overlapping commitments without crashing.
- Constraint-aware scheduling: Tasks are prioritized by available time budget and time conflicts are avoided during schedule generation.

These features ensure pet care plans are realistic, consistent, and conflict-free.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
