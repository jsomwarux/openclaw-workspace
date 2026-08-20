A super opens a work order on his phone, gets pulled into another issue, and comes back later to approve it.

In that window, the office closes the original work order and opens a new one for the same unit.

If the approval only knows the unit, it can land on the new record.

Nothing errors.

That is the dangerous version in operations. The approval is real. The audit trail looks clean. The system attached the work to the wrong record.

The action has to carry the exact record and the state the user saw when they approved it.

Now every approval carries:

- the work order ID
- the status the user approved from
- the action it is allowed to take

If the record has moved on, the system rejects the approval instead of guessing.

Open your work order history and find one approval that happened after the work order was already closed.

Then ask which record that approval actually touched.

#PropertyManagement #RealEstateOperations #OperationsManagement
