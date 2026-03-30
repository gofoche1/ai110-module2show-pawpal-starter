import pytest
from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


class TestTaskCompletion:
    """Tests for Task completion status."""

    def test_task_initial_status_pending(self):
        """Verify that a new task is marked as pending (not completed)."""
        task = Task(description="Walk", duration_minutes=30)
        assert task.completed is False

    def test_mark_completed_changes_status(self):
        """Verify that calling mark_completed() sets completed to True."""
        task = Task(description="Walk", duration_minutes=30)
        task.mark_completed()
        assert task.completed is True
        assert task.is_completed() is True

    def test_mark_pending_changes_status(self):
        """Verify that calling mark_pending() sets completed to False."""
        task = Task(description="Walk", duration_minutes=30, completed=True)
        task.mark_pending()
        assert task.completed is False
        assert task.is_completed() is False

    def test_toggle_completion_status(self):
        """Verify multiple toggles between pending and completed."""
        task = Task(description="Groom", duration_minutes=45)
        assert task.is_completed() is False

        task.mark_completed()
        assert task.is_completed() is True

        task.mark_pending()
        assert task.is_completed() is False

        task.mark_completed()
        assert task.is_completed() is True


class TestTaskAddition:
    """Tests for adding tasks to Pets."""

    def test_pet_starts_with_no_tasks(self):
        """Verify that a new Pet has an empty task list."""
        pet = Pet(name="Mochi", species="cat")
        assert len(pet.get_tasks()) == 0

    def test_adding_task_increases_count(self):
        """Verify that adding a task to a Pet increases task count."""
        pet = Pet(name="Buddy", species="dog")
        task = Task(description="Morning walk", duration_minutes=30)

        pet.add_task(task)

        assert len(pet.get_tasks()) == 1
        assert task in pet.get_tasks()

    def test_adding_multiple_tasks_increases_count(self):
        """Verify that adding multiple tasks increases count correctly."""
        pet = Pet(name="Fluffy", species="cat")
        task1 = Task(description="Feed", duration_minutes=10)
        task2 = Task(description="Play", duration_minutes=20)
        task3 = Task(description="Sleep", duration_minutes=60)

        pet.add_task(task1)
        assert len(pet.get_tasks()) == 1

        pet.add_task(task2)
        assert len(pet.get_tasks()) == 2

        pet.add_task(task3)
        assert len(pet.get_tasks()) == 3

    def test_get_tasks_returns_all_added_tasks(self):
        """Verify that get_tasks() returns all previously added tasks."""
        pet = Pet(name="Max", species="dog")
        tasks = [
            Task(description="Breakfast", duration_minutes=15),
            Task(description="Lunch", duration_minutes=15),
            Task(description="Dinner", duration_minutes=15),
        ]

        for task in tasks:
            pet.add_task(task)

        retrieved_tasks = pet.get_tasks()
        assert len(retrieved_tasks) == 3
        for task in tasks:
            assert task in retrieved_tasks

    def test_remove_task_decreases_count(self):
        """Verify that removing a task decreases the pet's task count."""
        pet = Pet(name="Rex", species="dog")
        task1 = Task(description="Walk", duration_minutes=30)
        task2 = Task(description="Play", duration_minutes=20)

        pet.add_task(task1)
        pet.add_task(task2)
        assert len(pet.get_tasks()) == 2

        pet.remove_task(task1)
        assert len(pet.get_tasks()) == 1
        assert task1 not in pet.get_tasks()
        assert task2 in pet.get_tasks()


class TestOwnerPetIntegration:
    """Tests for Owner and Pet interactions."""

    def test_owner_add_pet_increases_pet_count(self):
        """Verify that adding pets to Owner increases pet count."""
        owner = Owner(name="Jordan")
        assert len(owner.get_pets()) == 0

        pet1 = Pet(name="Mochi", species="cat")
        owner.add_pet(pet1)
        assert len(owner.get_pets()) == 1

        pet2 = Pet(name="Buddy", species="dog")
        owner.add_pet(pet2)
        assert len(owner.get_pets()) == 2

    def test_owner_get_all_tasks(self):
        """Verify that Owner can retrieve all tasks from all pets."""
        owner = Owner(name="Jordan")

        pet1 = Pet(name="Mochi", species="cat")
        pet2 = Pet(name="Buddy", species="dog")

        owner.add_pet(pet1)
        owner.add_pet(pet2)

        task1 = Task(description="Groom Mochi", duration_minutes=20)
        task2 = Task(description="Walk Buddy", duration_minutes=30)
        task3 = Task(description="Feed Mochi", duration_minutes=10)

        pet1.add_task(task1)
        pet1.add_task(task3)
        pet2.add_task(task2)

        all_tasks = owner.get_all_tasks()
        assert len(all_tasks) == 3
        assert task1 in all_tasks
        assert task2 in all_tasks
        assert task3 in all_tasks

    def test_owner_get_pending_tasks(self):
        """Verify that Owner can filter pending tasks from all pets."""
        owner = Owner(name="Jordan")
        pet = Pet(name="Mochi", species="cat")
        owner.add_pet(pet)

        task1 = Task(description="Groom", duration_minutes=20)
        task2 = Task(description="Feed", duration_minutes=10, completed=True)
        task3 = Task(description="Play", duration_minutes=15)

        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)

        pending = owner.get_all_pending_tasks()
        assert len(pending) == 2
        assert task1 in pending
        assert task3 in pending
        assert task2 not in pending

    def test_owner_get_completed_tasks(self):
        """Verify that Owner can filter completed tasks from all pets."""
        owner = Owner(name="Jordan")
        pet = Pet(name="Buddy", species="dog")
        owner.add_pet(pet)

        task1 = Task(description="Walk", duration_minutes=30, completed=True)
        task2 = Task(description="Play", duration_minutes=20)
        task3 = Task(description="Groom", duration_minutes=45, completed=True)

        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)

        completed = owner.get_all_completed_tasks()
        assert len(completed) == 2
        assert task1 in completed
        assert task3 in completed
        assert task2 not in completed


class TestSortingCorrectness:
    """Tests for task sorting by time (chronological order)."""

    def test_sort_by_time_single_task(self):
        """Verify that sorting a single task returns it unchanged."""
        scheduler = Scheduler()
        task = Task(description="Walk", duration_minutes=30, time="09:00")
        sorted_tasks = scheduler.sort_by_time([task])
        assert len(sorted_tasks) == 1
        assert sorted_tasks[0] == task

    def test_sort_by_time_ascending_order(self):
        """Verify tasks sort in ascending chronological order."""
        scheduler = Scheduler()
        task1 = Task(description="Morning walk", duration_minutes=30, time="08:00")
        task2 = Task(description="Lunch", duration_minutes=15, time="12:00")
        task3 = Task(description="Evening walk", duration_minutes=30, time="18:00")
        
        unsorted = [task3, task1, task2]
        sorted_tasks = scheduler.sort_by_time(unsorted)
        
        assert sorted_tasks[0] == task1
        assert sorted_tasks[1] == task2
        assert sorted_tasks[2] == task3

    def test_sort_by_time_reverse_order(self):
        """Verify tasks in reverse chronological order are sorted correctly."""
        scheduler = Scheduler()
        task1 = Task(description="Breakfast", duration_minutes=15, time="07:00")
        task2 = Task(description="Snack", duration_minutes=10, time="15:00")
        task3 = Task(description="Dinner", duration_minutes=20, time="19:00")
        
        unsorted = [task3, task2, task1]
        sorted_tasks = scheduler.sort_by_time(unsorted)
        
        assert sorted_tasks == [task1, task2, task3]

    def test_sort_by_time_with_empty_time_fields(self):
        """Verify tasks with empty time fields sort to the beginning."""
        scheduler = Scheduler()
        task_no_time1 = Task(description="Task A", duration_minutes=10, time="")
        task_with_time1 = Task(description="Task B", duration_minutes=15, time="10:00")
        task_no_time2 = Task(description="Task C", duration_minutes=20, time="")
        task_with_time2 = Task(description="Task D", duration_minutes=25, time="09:00")
        
        unsorted = [task_with_time1, task_no_time1, task_with_time2, task_no_time2]
        sorted_tasks = scheduler.sort_by_time(unsorted)
        
        # Tasks with empty time should come first (value 0)
        assert sorted_tasks[0].time == ""
        assert sorted_tasks[1].time == ""
        assert sorted_tasks[2].time == "09:00"
        assert sorted_tasks[3].time == "10:00"

    def test_sort_by_time_same_time_tasks(self):
        """Verify tasks at the same time maintain stable order."""
        scheduler = Scheduler()
        task1 = Task(description="Walk 1", duration_minutes=30, time="09:00")
        task2 = Task(description="Walk 2", duration_minutes=30, time="09:00")
        task3 = Task(description="Walk 3", duration_minutes=30, time="09:00")
        
        unsorted = [task3, task1, task2]
        sorted_tasks = scheduler.sort_by_time(unsorted)
        
        assert len(sorted_tasks) == 3
        assert sorted_tasks[0].time == "09:00"
        assert sorted_tasks[1].time == "09:00"
        assert sorted_tasks[2].time == "09:00"

    def test_sort_by_time_midnight_edge_case(self):
        """Verify midnight (00:00) sorts before morning tasks."""
        scheduler = Scheduler()
        task_midnight = Task(description="Midnight snack", duration_minutes=10, time="00:00")
        task_morning = Task(description="Breakfast", duration_minutes=15, time="08:00")
        task_evening = Task(description="Dinner", duration_minutes=20, time="20:00")
        
        unsorted = [task_evening, task_midnight, task_morning]
        sorted_tasks = scheduler.sort_by_time(unsorted)
        
        assert sorted_tasks[0] == task_midnight
        assert sorted_tasks[1] == task_morning
        assert sorted_tasks[2] == task_evening

    def test_sort_by_time_various_hours(self):
        """Verify sorting with various single-digit and double-digit hours."""
        scheduler = Scheduler()
        tasks = [
            Task(description="Task A", duration_minutes=10, time="23:00"),
            Task(description="Task B", duration_minutes=10, time="01:00"),
            Task(description="Task C", duration_minutes=10, time="13:30"),
            Task(description="Task D", duration_minutes=10, time="08:15"),
        ]
        
        sorted_tasks = scheduler.sort_by_time(tasks)
        
        assert sorted_tasks[0].time == "01:00"
        assert sorted_tasks[1].time == "08:15"
        assert sorted_tasks[2].time == "13:30"
        assert sorted_tasks[3].time == "23:00"


class TestRecurrenceLogic:
    """Tests for recurring task logic."""

    def test_daily_task_completion_creates_next_day_task(self):
        """Verify marking a daily task complete creates a new task for the next day."""
        pet = Pet(name="Buddy", species="dog")
        original_date = date.today()
        task = Task(
            description="Morning walk",
            duration_minutes=30,
            frequency="daily",
            time="08:00",
            due_date=original_date
        )
        pet.add_task(task)
        
        scheduler = Scheduler()
        scheduler.mark_task_complete(pet, task)
        
        # Original task should be marked complete
        assert task.completed is True
        
        # New task should be created for next day
        all_tasks = pet.get_tasks()
        assert len(all_tasks) == 2
        
        new_task = all_tasks[1]
        assert new_task.description == task.description
        assert new_task.duration_minutes == task.duration_minutes
        assert new_task.frequency == "daily"
        assert new_task.completed is False
        assert new_task.due_date == original_date + timedelta(days=1)
        assert new_task.time == "08:00"

    def test_weekly_task_completion_creates_next_week_task(self):
        """Verify marking a weekly task complete creates a new task for the next week."""
        pet = Pet(name="Fluffy", species="cat")
        original_date = date.today()
        task = Task(
            description="Vet checkup",
            duration_minutes=60,
            frequency="weekly",
            time="14:00",
            due_date=original_date
        )
        pet.add_task(task)
        
        scheduler = Scheduler()
        scheduler.mark_task_complete(pet, task)
        
        # Original task should be marked complete
        assert task.completed is True
        
        # New task should be created for next week (7 days later)
        all_tasks = pet.get_tasks()
        assert len(all_tasks) == 2
        
        new_task = all_tasks[1]
        assert new_task.description == task.description
        assert new_task.frequency == "weekly"
        assert new_task.completed is False
        assert new_task.due_date == original_date + timedelta(days=7)
        assert new_task.time == "14:00"

    def test_once_frequency_task_does_not_recur(self):
        """Verify that tasks with frequency='once' do not create new occurrences."""
        pet = Pet(name="Max", species="dog")
        task = Task(
            description="One-time appointment",
            duration_minutes=45,
            frequency="once",
            due_date=date.today()
        )
        pet.add_task(task)
        
        scheduler = Scheduler()
        scheduler.mark_task_complete(pet, task)
        
        # Only original task should exist
        assert len(pet.get_tasks()) == 1
        assert pet.get_tasks()[0].completed is True

    def test_daily_task_recurrence_across_month_boundary(self):
        """Verify daily recurrence handles month boundaries correctly."""
        pet = Pet(name="Buddy", species="dog")
        # Jan 31, 2026
        task = Task(
            description="Daily feed",
            duration_minutes=10,
            frequency="daily",
            due_date=date(2026, 1, 31)
        )
        pet.add_task(task)
        
        scheduler = Scheduler()
        scheduler.mark_task_complete(pet, task)
        
        new_task = pet.get_tasks()[1]
        # Should be Feb 1, 2026
        assert new_task.due_date == date(2026, 2, 1)

    def test_weekly_task_recurrence_across_year_boundary(self):
        """Verify weekly recurrence handles year boundaries correctly."""
        pet = Pet(name="Fluffy", species="cat")
        # Dec 28, 2025 (7 days later is Jan 4, 2026)
        task = Task(
            description="Weekly grooming",
            duration_minutes=30,
            frequency="weekly",
            due_date=date(2025, 12, 28)
        )
        pet.add_task(task)
        
        scheduler = Scheduler()
        scheduler.mark_task_complete(pet, task)
        
        new_task = pet.get_tasks()[1]
        # Should be Jan 4, 2026
        assert new_task.due_date == date(2026, 1, 4)

    def test_recurring_task_inherits_all_attributes(self):
        """Verify that recurring task inherits description, duration, frequency, and time."""
        pet = Pet(name="Mochi", species="cat")
        original_task = Task(
            description="Special feeding",
            duration_minutes=25,
            frequency="daily",
            time="12:30",
            due_date=date.today()
        )
        pet.add_task(original_task)
        
        scheduler = Scheduler()
        scheduler.mark_task_complete(pet, original_task)
        
        new_task = pet.get_tasks()[1]
        assert new_task.description == "Special feeding"
        assert new_task.duration_minutes == 25
        assert new_task.frequency == "daily"
        assert new_task.time == "12:30"

    def test_multiple_sequential_completions_create_chain(self):
        """Verify that completing recurring tasks multiple times creates a chain."""
        pet = Pet(name="Buddy", species="dog")
        base_date = date(2026, 3, 1)
        task = Task(
            description="Daily walk",
            duration_minutes=30,
            frequency="daily",
            due_date=base_date
        )
        pet.add_task(task)
        
        scheduler = Scheduler()
        
        # Complete first task
        scheduler.mark_task_complete(pet, task)
        assert len(pet.get_tasks()) == 2
        assert pet.get_tasks()[0].due_date == base_date
        assert pet.get_tasks()[1].due_date == base_date + timedelta(days=1)
        
        # Complete second task
        second_task = pet.get_tasks()[1]
        scheduler.mark_task_complete(pet, second_task)
        assert len(pet.get_tasks()) == 3
        assert pet.get_tasks()[2].due_date == base_date + timedelta(days=2)


class TestConflictDetection:
    """Tests for time conflict detection."""

    def test_no_conflict_empty_task_list(self):
        """Verify no conflicts detected in empty task list."""
        scheduler = Scheduler()
        warning = scheduler.detect_time_conflicts([])
        assert warning == ""

    def test_no_conflict_single_task(self):
        """Verify no conflicts when only one task exists."""
        scheduler = Scheduler()
        task = Task(description="Walk", duration_minutes=30, time="09:00")
        warning = scheduler.detect_time_conflicts([task])
        assert warning == ""

    def test_no_conflict_different_times(self):
        """Verify no conflicts when tasks have different times."""
        scheduler = Scheduler()
        task1 = Task(description="Morning walk", duration_minutes=30, time="08:00")
        task2 = Task(description="Lunch", duration_minutes=15, time="12:00")
        task3 = Task(description="Evening walk", duration_minutes=30, time="18:00")
        
        warning = scheduler.detect_time_conflicts([task1, task2, task3])
        assert warning == ""

    def test_conflict_two_tasks_same_time(self):
        """Verify conflict detected when two tasks have the same time."""
        scheduler = Scheduler()
        task1 = Task(description="Walk Buddy", duration_minutes=30, time="09:00")
        task2 = Task(description="Walk Mochi", duration_minutes=30, time="09:00")
        
        warning = scheduler.detect_time_conflicts([task1, task2])
        assert "Warning: Time conflicts detected:" in warning
        assert "09:00" in warning

    def test_conflict_multiple_tasks_same_time(self):
        """Verify all conflicts detected when multiple tasks share the same time."""
        scheduler = Scheduler()
        task1 = Task(description="Walk 1", duration_minutes=30, time="09:00")
        task2 = Task(description="Walk 2", duration_minutes=30, time="09:00")
        task3 = Task(description="Walk 3", duration_minutes=30, time="09:00")
        
        warning = scheduler.detect_time_conflicts([task1, task2, task3])
        assert "Warning: Time conflicts detected:" in warning
        assert "09:00" in warning

    def test_conflict_multiple_conflict_pairs(self):
        """Verify all conflict pairs are reported."""
        scheduler = Scheduler()
        task1 = Task(description="Task A", duration_minutes=15, time="10:00")
        task2 = Task(description="Task B", duration_minutes=15, time="10:00")
        task3 = Task(description="Task C", duration_minutes=20, time="14:00")
        task4 = Task(description="Task D", duration_minutes=20, time="14:00")
        
        warning = scheduler.detect_time_conflicts([task1, task2, task3, task4])
        assert "Warning: Time conflicts detected:" in warning
        assert "10:00" in warning
        assert "14:00" in warning

    def test_no_conflict_empty_time_fields(self):
        """Verify tasks with empty time fields do not create conflicts."""
        scheduler = Scheduler()
        task1 = Task(description="Task A", duration_minutes=10, time="")
        task2 = Task(description="Task B", duration_minutes=10, time="")
        task3 = Task(description="Task C", duration_minutes=10, time="09:00")
        
        warning = scheduler.detect_time_conflicts([task1, task2, task3])
        assert warning == ""

    def test_conflict_ignores_empty_time_fields(self):
        """Verify empty time fields are ignored; only non-empty times conflict."""
        scheduler = Scheduler()
        task_no_time = Task(description="Task without time", duration_minutes=10, time="")
        task1 = Task(description="Task at 09:00", duration_minutes=15, time="09:00")
        task2 = Task(description="Another task at 09:00", duration_minutes=15, time="09:00")
        
        warning = scheduler.detect_time_conflicts([task_no_time, task1, task2])
        assert "Warning: Time conflicts detected:" in warning
        assert "09:00" in warning

    def test_conflict_detection_with_completed_tasks(self):
        """Verify conflict detection works regardless of task completion status."""
        scheduler = Scheduler()
        task1 = Task(description="Walk", duration_minutes=30, time="09:00", completed=True)
        task2 = Task(description="Groom", duration_minutes=45, time="09:00", completed=False)
        
        warning = scheduler.detect_time_conflicts([task1, task2])
        assert "Warning: Time conflicts detected:" in warning

    def test_conflict_message_includes_task_descriptions(self):
        """Verify conflict message includes both task descriptions and time."""
        scheduler = Scheduler()
        task1 = Task(description="Morning walk", duration_minutes=30, time="08:00")
        task2 = Task(description="Breakfast prep", duration_minutes=15, time="08:00")
        
        warning = scheduler.detect_time_conflicts([task1, task2])
        assert "Morning walk" in warning
        assert "Breakfast prep" in warning
        assert "08:00" in warning

