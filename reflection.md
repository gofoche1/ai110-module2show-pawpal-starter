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
   Yes, my design changed during implementation. One important change was defining the relationships more clearly:
        Pet references Owner
        Task references Pet
        Owner references Pet through a list of pets
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
I felt this tradeoff was reasonable because it kept the implementation simple, understandable, and appropriate for a minimum product.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI during this project for design brainstorming, debugging, and refactoring. It was especially helpful when I wanted to think through class relationships, improve logic, and clarify how different parts of the scheduler should interact.
- What kinds of prompts or questions were most helpful?
“Why is this logic failing?”
“What edge cases should I test for this scheduler?”
**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
The tasks should have been sorted in chronological order (07:00, 15:00, 19:00), but the AI-generated assertion listed them in the wrong order.
- How did you evaluate or verify what the AI suggested?
I verified this by comparing the expected output with the actual scheduling logic and checking the sorted task times myself.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
Correct creation of owners, pets, and tasks
Proper assignment of pets to owners
Task sorting in chronological order
Conflict detection when tasks share the same time slot
- Why were these tests important?
Because they checked both the correctness of the class relationships and the core scheduling functionality.

**b. Confidence**

- How confident are you that your scheduler works correctly?
 (3.4 / 5.0)
The system demonstrates solid core functionality with well-tested sorting, recurrence, and conflict detection. However, reliability confidence is moderate due to time conflict resolution strategy not implemented (conflicts detected but not resolved)

- What edge cases would you test next if you had more time?
Boundary conditions for time values
Invalid or missing input data
Multiple overlapping tasks
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am most satisfied with is the overall class structure and how the system models the relationships between owners, pets, and tasks
**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
 I would improve the scheduler by making conflict handling more advanced. Instead of only warning about conflicts.
**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
I learned from this project is that good system design requires both planning and flexibility. One key lesson I learned is that even with powerful AI tools, I still need to act as the lead architect of the system. AI can generate ideas, code, and suggestions quickly, but it does not fully understand the intent or design goals. It is my responsibility to evaluate, verify, and decide what fits the system.

The most effective Copilot features for building my scheduler were code suggestions/autocomplete and inline explanations.
Using separate chat sessions for different phases (design, implementation, debugging, and testing) helped me stay organized and focused. This separation prevented confusion, reduced context overload, and made it easier to track decisions at each stage.