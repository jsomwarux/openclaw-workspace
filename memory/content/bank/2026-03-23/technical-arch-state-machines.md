# technical-arch-state-machines
# Pass 2: Technical post
# angle_id: arch-state-machines
# platform: X | banked: true | posted: false

conversational agents accumulate context debt over long tasks.

state machines don't.

read state.json. execute one step. write state.json. if it fails, restart from the last known state.

predictable. debuggable. resumes correctly after failure.

most agent reliability problems are solved by switching from conversational to state machine.
