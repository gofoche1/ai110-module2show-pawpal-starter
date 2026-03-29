from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        pass

    def get_pets(self) -> list[Pet]:
        pass


@dataclass
class Pet:
    name: str
    species: str
    owner: Owner
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def get_tasks(self) -> list[Task]:
        pass


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    pet: Pet

    def get_duration(self) -> int:
        pass

    def get_priority(self) -> str:
        pass


@dataclass
class WalkTask(Task):
    location: str


@dataclass
class Schedule:
    tasks: list[Task] = field(default_factory=list)
    total_time: int = 0

    def add_task(self, task: Task):
        pass

    def get_total_time(self) -> int:
        pass

    def get_tasks(self) -> list[Task]:
        pass


class Scheduler:
    def generate_schedule(self, pet: Pet, tasks: list[Task], available_time: int) -> Schedule:
        pass

    def schedule_walk(self, pet: Pet, walk_task: WalkTask, time_slot: str) -> bool:
        pass
