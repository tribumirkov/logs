# Project Workflow

## Guiding Principles

1. **The Plan is the Source of Truth:** All work must be tracked in `plan.md`
2. **The Tech Stack is Deliberate:** Changes to the tech stack must be documented in `tech-stack.md` *before* implementation
3. **Strict PEP 8 Adherence:** Code must strictly follow PEP 8 standards.
4. **No Unit Testing:** For this POC, unit testing is explicitly excluded to prioritize rapid implementation and strict linting.
5. **Strict Linting Enforcement:** `pylint` must be executed after every code generation or modification to ensure quality and style compliance.
6. **Environment Management with `uv`:** All dependency management and script execution must use `uv`.
7. **User Experience First:** Every decision should prioritize user experience.
8. **Non-Interactive & CI-Aware:** Prefer non-interactive commands. Use `CI=true` for watch-mode tools.

## Task Workflow

All tasks follow a strict lifecycle:

### Standard Task Workflow

1. **Select Task:** Choose the next available task from `plan.md` in sequential order

2. **Mark In Progress:** Before beginning work, edit `plan.md` and change the task from `[ ]` to `[~]`

3. **Implement Feature:**
   - Write the application code according to the task description.
   - Use `uv run` for any execution or script running.

4. **Strict Linting (PEP 8):**
   - Run `pylint` on the modified files:
     ```bash
     uv run pylint <file_or_directory>
     ```
   - **CRITICAL:** All linting errors and warnings must be resolved before proceeding.

5. **Document Deviations:** If implementation differs from tech stack:
   - **STOP** implementation
   - Update `tech-stack.md` with new design
   - Add dated note explaining the change
   - Resume implementation

6. **Commit Code Changes:**
   - Stage all code changes related to the task.
   - Propose a clear, concise commit message e.g, `feat(data): Implement synthetic log generator`.
   - Perform the commit.

7. **Attach Task Summary with Git Notes:**
   - **Step 7.1: Get Commit Hash:** Obtain the hash of the *just-completed commit* (`git log -1 --format="%H"`).
   - **Step 7.2: Draft Note Content:** Create a detailed summary for the completed task.
   - **Step 7.3: Attach Note:** Use the `git notes` command to attach the summary to the commit.
     ```bash
     git notes add -m "<note content>" <commit_hash>
     ```

8. **Get and Record Task Commit SHA:**
    - **Step 8.1: Update Plan:** Read `plan.md`, find the line for the completed task, update its status from `[~]` to `[x]`, and append the first 7 characters of the *just-completed commit's* commit hash.
    - **Step 8.2: Write Plan:** Write the updated content back to `plan.md`.

9. **Commit Plan Update:**
    - **Action:** Stage the modified `plan.md` file.
    - **Action:** Commit this change with a descriptive message.

### Phase Completion Verification and Checkpointing Protocol

**Trigger:** This protocol is executed immediately after a task is completed that also concludes a phase in `plan.md`.

1.  **Announce Protocol Start:** Inform the user that the phase is complete and the verification and checkpointing protocol has begun.

2.  **Verify Phase Quality:**
    -   Run `pylint` on all files modified in the phase.
    -   Address any accumulated style or quality issues.

3.  **Propose a Detailed, Actionable Manual Verification Plan:**
    -   Generate a step-by-step plan for the user to verify the phase's outcomes manually.
    -   **PAUSE** and await the user's response: "**Does this meet your expectations? Please confirm with yes or provide feedback on what needs to be changed.**"

4.  **Create Checkpoint Commit:**
    -   Stage all changes.
    -   Perform the commit with a message like `conductor(checkpoint): Checkpoint end of Phase X`.

5.  **Attach Auditable Verification Report using Git Notes:**
    -   Attach the verification steps and user confirmation as a git note.

6.  **Get and Record Phase Checkpoint SHA:**
    -   Update `plan.md` with the checkpoint hash.

7. **Commit Plan Update:**
    - Stage and commit the updated `plan.md`.

8.  **Announce Completion:** Inform the user that the phase is complete and the checkpoint has been created.

## Quality Gates

Before marking any task complete, verify:

- [ ] Code follows PEP 8 via `pylint` (Zero errors/warnings)
- [ ] All public functions/methods are documented with docstrings
- [ ] Type hints are used throughout
- [ ] Environment and dependencies managed via `uv`
- [ ] Documentation updated if needed

## Development Commands

### Setup
```bash
# Initialize environment and install dependencies
uv init
uv add pylint pyyaml numpy pandas scikit-learn sentence-transformers torch
```

### Daily Development
```bash
# Run a script
uv run python <script.py>

# Linting
uv run pylint <file_or_directory>
```

## Commit Guidelines

### Message Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `chore`: Maintenance tasks

## Definition of Done

A task is complete when:

1. All code implemented to specification
2. `pylint` passes with no issues
3. Documentation complete (docstrings)
4. Changes committed with proper message
5. Git note with task summary attached to the commit