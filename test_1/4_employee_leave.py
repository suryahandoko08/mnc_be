from datetime import datetime, timedelta

def can_take_personal_leave(total_joint_leave, join_date, planned_leave_date, leave_duration):

    join_date = datetime.strptime(join_date, '%Y-%m-%d')
    planned_leave_date = datetime.strptime(planned_leave_date, '%Y-%m-%d')

    if planned_leave_date < join_date + timedelta(days=180):
        return False, "Reason: Not eligible for personal leave yet (within 180 days of joining)."

    eligibility_start_date = join_date + timedelta(days=180)

    days_until_end_of_year = (datetime(year=eligibility_start_date.year, month=12, day=31) - eligibility_start_date).days + 1
    
    personal_leave_quota = (days_until_end_of_year * total_joint_leave) 

    if leave_duration > personal_leave_quota:
        return False, f"Reason: Can only take {personal_leave_quota} day(s) of personal leave."
    
    if leave_duration > 3:
        return False, "Reason: Maximum allowed personal leave is 3 consecutive days."

    return True, "Leave can be taken."

# Example usage
print(can_take_personal_leave(7, '2021-05-01', '2021-07-05', 1))  # Output: (False, "Reason: Not eligible...")
print(can_take_personal_leave(7, '2021-05-01', '2021-11-05', 3))  # Output: (False, "Reason: Can only take...")
print(can_take_personal_leave(7, '2021-01-05', '2021-12-18', 1))  # Output: (True, "Leave can be taken.")
print(can_take_personal_leave(7, '2021-01-05', '2021-12-18', 3))  # Output: (True, "Leave can be taken.")
