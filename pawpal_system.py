from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    description: str
    duration_minutes: int
    frequency: str = "once"  # e.g. "daily", "weekly", "once"
    completed: bool = False

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
        return f"{self.description} ({self.duration_minutes}m, {self.frequency}, {status})"


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
    def generate_schedule(self, pet: Pet, available_time: int) -> Schedule:
        """Create a schedule for a single pet's pending tasks within available time."""
        schedule = Schedule()
        for task in sorted(pet.get_pending_tasks(), key=lambda t: t.duration_minutes):
            if schedule.total_time + task.duration_minutes <= available_time:
                schedule.add_task(task)
        return schedule

    def generate_owner_schedule(self, owner: Owner, available_time: int) -> Schedule:
        """Create a schedule for all of an owner's pets' pending tasks within available time."""
        schedule = Schedule()
        all_tasks = owner.get_all_pending_tasks()

        # Example prioritization: shorter tasks first, for higher throughput
        for task in sorted(all_tasks, key=lambda t: t.duration_minutes):
            if schedule.total_time + task.duration_minutes <= available_time:
                schedule.add_task(task)

        return schedule

    def schedule_walk(self, pet: Pet, walk_task: Task, time_slot: str) -> bool:
        """Add a walk task to a pet's schedule for a specific time slot."""
        if walk_task not in pet.tasks:
            pet.add_task(walk_task)

        # In a more advanced design, we'd verify time_slot against a daily
        # calendar object; here, we attach the task and accept for now.
        return True

    def get_tasks_by_pet(self, owner: Owner) -> dict[str, list[Task]]:
        """Return a dictionary mapping each pet's name to its task list."""
        tasks_by_pet = {}
        for pet in owner.get_pets():
            tasks_by_pet[pet.name] = pet.get_tasks()
        return tasks_by_pet

    def summarize_owner_tasks(self, owner: Owner) -> str:
        """Return a summary string of pending and completed tasks for an owner."""
        pending = owner.get_all_pending_tasks()
        completed = owner.get_all_completed_tasks()
        return (
            f"Owner {owner.name}: {len(pending)} pending tasks, "
            f"{len(completed)} completed tasks across {len(owner.pets)} pets."
        )
