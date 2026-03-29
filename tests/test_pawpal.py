import pytest
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
