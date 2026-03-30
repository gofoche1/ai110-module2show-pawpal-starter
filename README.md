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

## Testing PawPal+

### Running Tests

To execute the test suite, run:

```bash
python -m pytest tests/test_pawpal.py -v
```

### Test Coverage

The test suite comprehensively validates the following critical areas:

**Sorting Correctness (7 tests)**
- Verifies tasks are returned in chronological order by time (HH:MM format)
- Handles edge cases including empty time fields, midnight boundaries, and tasks with identical times
- Ensures consistent, predictable ordering for daily planning

**Recurrence Logic (7 tests)**
- Confirms marking a daily task complete creates a new task for the following day
- Validates weekly recurrence logic with 7-day intervals
- Tests boundary conditions (month/year transitions) and attribute inheritance for recurring tasks
- Ensures one-time tasks don't create unwanted recurrences

**Conflict Detection (9 tests)**
- Detects tasks scheduled at the same time and produces warning messages
- Handles multiple conflict scenarios with multiple task pairs
- Ignores empty/unscheduled time fields appropriately
- Verifies conflict messages include descriptive task information

**Additional Coverage**
- Task completion status management (pending/completed toggling)
- Task addition and removal from pets
- Owner-pet integration and multi-pet task aggregation
- Task filtering by completion status and pet name

### Confidence Level

**★★★☆☆ (3.4 / 5.0)**

The system demonstrates solid core functionality with well-tested sorting, recurrence, and conflict detection. However, reliability confidence is moderate due to:

- **Strengths**: Critical scheduling features are thoroughly validated; edge cases like month boundaries and time conflicts are covered
- **Limitations**: Real-world scenario testing (e.g., large task volumes, rapid state changes) is limited; UI integration not directly tested; time conflict resolution strategy not implemented (conflicts detected but not resolved)
- **Future work**: Add integration tests with full workflow scenarios, implement conflict resolution strategies, validate performance with large datasets, and test Streamlit UI interaction


## Smarter Scheduling Algorithms

Your PawPal+ system implements the following core scheduling and management algorithms:

### **1. Time-Based Chronological Sorting**
- **Method:** `Scheduler.sort_by_time(tasks)` + time-aware sorting in `generate_owner_schedule()`
- **Details:** Tasks sorted by scheduled time (HH:MM format) in 24-hour format; handles empty time fields gracefully; used to create clear, ordered daily plans
- **Use case:** Owner sees tasks in order they'll happen throughout the day

### **2. Intelligent Task Filtering**
- **Method:** `Scheduler.filter_tasks(owner, completion_status, pet_name)`
- **Details:** Filter by completion status (pending/completed/all) and/or specific pet; enables quick views of what needs attention
- **Use case:** "Show me all pending tasks for Buddy" or "What has Mochi completed today?"

### **3. Recurring Task Automation**
- **Method:** `Scheduler.mark_task_complete(pet, task)`
- **Details:** When a recurring task (daily/weekly) is marked complete, automatically generates next occurrence with updated due date using `timedelta`; one-time tasks don't recur
- **Use case:** Mark "Morning walk" complete → system creates tomorrow's walk automatically

### **4. Time Conflict Detection**
- **Method:** `Scheduler.detect_time_conflicts(tasks)`
- **Details:** Identifies tasks scheduled at identical times; produces descriptive warning messages; prevents overlapping commitments
- **Use case:** Warns "Morning walk and playtime at 09:00 conflict"

### **5. Time-Aware Schedule Generation**
- **Method:** `Scheduler.generate_owner_schedule(owner, available_time)`
- **Details:** Builds daily schedule respecting time budget; sorts by chronological time, then duration; avoids scheduling conflicting tasks
- **Use case:** "Create today's plan with 2 hours available" → avoids conflicts and stays within time limit

### **6. Multi-Pet Task Aggregation & Querying**
- **Method:** `Owner.get_all_tasks()`, `Owner.get_all_pending_tasks()`, `Owner.get_all_completed_tasks()`, `Scheduler.get_tasks_by_pet()`
- **Details:** Unified view of tasks across all pets; quickly answer "What needs to happen today?" and "Which pet needs what?"
- **Use case:** Comprehensive owner dashboard showing all pet care needs

### **7. Task State Management (Recurrence & Completion)**
- **Method:** `Task.mark_completed()`, `Task.mark_pending()`, `Task.is_completed()`
- **Details:** Track task completion with automatic recurrence generation; supports daily, weekly, and one-time frequencies
- **Use case:** Toggle task status while system maintains recurring schedule automatically

<a href="/images/demo.png" target="_blank"><img src='/images/demo.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.