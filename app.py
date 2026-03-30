import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler, Schedule

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
# Persist owner state across reruns
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner: Owner = st.session_state.owner
st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a daily schedule based on your pet's tasks.")

# Update owner name if changed
owner.name = owner_name

# Get or create pet
pets_dict = {p.name: p for p in owner.get_pets()}
if pet_name not in pets_dict:
    new_pet = Pet(name=pet_name, species=species)
    owner.add_pet(new_pet)
    st.session_state.owner = owner
else:
    new_pet = pets_dict[pet_name]

# Add tasks from UI to pet
for task_dict in st.session_state.tasks:
    task = Task(
        description=task_dict["title"],
        duration_minutes=task_dict["duration_minutes"],
        frequency="once"
    )
    # Only add if not already in pet's task list
    if task not in new_pet.tasks:
        new_pet.add_task(task)

available_time = st.slider("Available time (minutes)", 30, 480, 120)

if st.button("Generate schedule"):
    if not st.session_state.tasks:
        st.warning("Please add at least one task first.")
    else:
        scheduler = Scheduler()
        schedule = scheduler.generate_owner_schedule(owner=owner, available_time=available_time)
        
        st.success("✅ Schedule Generated!")
        
        if schedule.tasks:
            st.markdown("### 📅 Today's Plan")
            
            for idx, task in enumerate(schedule.tasks, start=1):
                st.write(f"**{idx}. {task.description}**")
                st.write(f"   ⏱️ Duration: {task.duration_minutes} min | 🔄 {task.frequency}")
            
            st.divider()
            st.metric("Total Time Scheduled", f"{schedule.total_time} minutes", f"Available: {available_time} min")
            
            # Show summary
            st.markdown("### 📊 Summary")
            st.write(scheduler.summarize_owner_tasks(owner))
        else:
            st.info("No tasks fit within the available time. Try increasing available time or reducing task durations.")
