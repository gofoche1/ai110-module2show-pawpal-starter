# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
OWNER class stores the name and pet name allows funtion to add pet,
 PET class name, species and tasks, 
 Tasks class priorty,pet and duration
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
    Yes it did, Pet references Owner, Task references Pet, and Owner references Pet via list. This is fine with forward annotations, but instantiation order matters (create Owner first, then Pet with owner, then add pet to owner). Add validation for dataclasses (e.g., check priority values).

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
available_time, Task duration, scheduled time for chronological sort and conflict detection (same time slot across tasks)
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
A lightweight conflict-warning approach is chosen over full CSP/inference 
to keep implementation simple and safe for MVP.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
 it made a logic error. The assertion is incorrect. The tasks should be sorted in chronological order (07:00, 15:00, 19:00), but I asserted them in the wrong order
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
the boundaries and  validate performance with large datasets
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
