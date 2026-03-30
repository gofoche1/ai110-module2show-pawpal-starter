from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple
from datetime import date, timedelta


@dataclass
class Task:
    description: str
    duration_minutes: int
    frequency: str = "once"  # e.g. "daily", "weekly", "once"
    completed: bool = False
    time: str = ""  # e.g. "09:00" for 9 AM
    due_date: date = field(default_factory=date.today)

    def mark_completed(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def mark_pending(self) -> None:
        """Mark this task as pending (not completed)."""
        self.completed = False

    def is_completed(self) -> bool:
        """Return True if this task is completed."""
        return self.completed

    def __str__(self):
        """Return a formatted string representation of the task."""
        status = "Done" if self.completed else "Pending"
        return f"{self.description} ({self.duration_minutes}m, {self.frequency}, {status}, due: {self.due_date})"


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list if it exists."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        """Return a copy of all tasks for this pet."""
        return list(self.tasks)

    def get_pending_tasks(self) -> List[Task]:
        """Return all pending (incomplete) tasks for this pet."""
        return [task for task in self.tasks if not task.completed]

    def get_completed_tasks(self) -> List[Task]:
        """Return all completed tasks for this pet."""
        return [task for task in self.tasks if task.completed]


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def get_pets(self) -> List[Pet]:
        """Return a copy of all pets owned by this owner."""
        return list(self.pets)

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks from all pets owned by this owner."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks())
        return tasks

    def get_all_pending_tasks(self) -> List[Task]:
        """Return all pending tasks from all pets owned by this owner."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_pending_tasks())
        return tasks

    def get_all_completed_tasks(self) -> List[Task]:
        """Return all completed tasks from all pets owned by this owner."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_completed_tasks())
        return tasks


# Keep Schedule and Scheduler stubs for later expansion
@dataclass
class Schedule:
    tasks: List[Task] = field(default_factory=list)
    total_time: int = 0

    def add_task(self, task: Task) -> None:
        """Add a task to the schedule and update total time."""
        self.tasks.append(task)
        self.total_time += task.duration_minutes

    def get_total_time(self) -> int:
        """Return the total duration in minutes of all scheduled tasks."""
        return self.total_time

    def get_tasks(self) -> List[Task]:
        """Return a copy of all tasks in this schedule."""
        return list(self.tasks)


class Scheduler:
    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by their time attribute in HH:MM format."""
        return sorted(tasks, key=lambda t: int(t.time.split(':')[0]) * 60 + int(t.time.split(':')[1]) if t.time else 0)

    def filter_tasks(self, owner: Owner, completion_status: bool | None = None, pet_name: str | None = None) -> List[Task]:
        """Filter tasks by completion status and/or pet name.
        
        Args:
            owner: The owner whose tasks to filter.
            completion_status: True for completed, False for pending, None for all.
            pet_name: Name of the pet to filter by, None for all pets.
        
        Returns:
            List of filtered tasks.
        """
        tasks = []
        for pet in owner.get_pets():
            if pet_name is None or pet.name == pet_name:
                pet_tasks = pet.get_tasks()
                if completion_status is not None:
                    pet_tasks = [t for t in pet_tasks if t.completed == completion_status]
                tasks.extend(pet_tasks)
        return tasks

    def mark_task_complete(self, pet: Pet, task: Task) -> None:
        """Mark a task as completed and create next occurrence if recurring."""
        task.mark_completed()
        if task.frequency == "daily":
            new_due_date = task.due_date + timedelta(days=1)
            new_task = Task(
                description=task.description,
                duration_minutes=task.duration_minutes,
                frequency=task.frequency,
                time=task.time,
                due_date=new_due_date
            )
            pet.add_task(new_task)
        elif task.frequency == "weekly":
            new_due_date = task.due_date + timedelta(days=7)
            new_task = Task(
                description=task.description,
                duration_minutes=task.duration_minutes,
                frequency=task.frequency,
                time=task.time,
                due_date=new_due_date
            )
            pet.add_task(new_task)

    def detect_time_conflicts(self, tasks: List[Task]) -> str:
        """Detect tasks that are scheduled at the same time and return a warning message.
        
        Returns an empty string if no conflicts, otherwise a warning message.
        """
        conflicts = []
        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                if tasks[i].time == tasks[j].time and tasks[i].time:
                    conflicts.append((tasks[i], tasks[j]))
        if conflicts:
            conflict_descriptions = [f"{t1.description} and {t2.description} at {t1.time}" for t1, t2 in conflicts]
            return f"Warning: Time conflicts detected: {', '.join(conflict_descriptions)}"
        return ""

    def generate_schedule(self, pet: Pet, available_time: int) -> Schedule:
        schedule = Schedule()
        for task in sorted(pet.get_pending_tasks(), key=lambda t: t.duration_minutes):
            if schedule.total_time + task.duration_minutes <= available_time:
                schedule.add_task(task)
        return schedule

    def generate_owner_schedule(self, owner: Owner, available_time: int) -> Schedule:
        schedule = Schedule()
        all_tasks = owner.get_all_pending_tasks()

        # Sort by time first, then by duration for tie-breaking
        sorted_tasks = sorted(all_tasks, key=lambda t: (int(t.time.split(':')[0]) * 60 + int(t.time.split(':')[1]) if t.time else 0, t.duration_minutes))

        for task in sorted_tasks:
            if schedule.total_time + task.duration_minutes <= available_time:
                # Check for time conflicts with already scheduled tasks
                temp_tasks = schedule.tasks + [task]
                warning = self.detect_time_conflicts(temp_tasks)
                if not warning:  # No conflicts
                    schedule.add_task(task)

        return schedule

    def schedule_walk(self, pet: Pet, walk_task: Task, time_slot: str) -> bool:
        if walk_task not in pet.tasks:
            pet.add_task(walk_task)

        # In a more advanced design, we'd verify time_slot against a daily
        # calendar object; here, we attach the task and accept for now.
        return True

    def get_tasks_by_pet(self, owner: Owner) -> dict[str, list[Task]]:
        tasks_by_pet = {}
        for pet in owner.get_pets():
            tasks_by_pet[pet.name] = pet.get_tasks()
        return tasks_by_pet

    def summarize_owner_tasks(self, owner: Owner) -> str:
        pending = owner.get_all_pending_tasks()
        completed = owner.get_all_completed_tasks()
        return (
            f"Owner {owner.name}: {len(pending)} pending tasks, "
            f"{len(completed)} completed tasks across {len(owner.pets)} pets."
        )
