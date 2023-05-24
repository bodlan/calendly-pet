import calendar


def generate_calendar(year, month):
    cal = calendar.monthcalendar(year, month)
    # Update days before the actual month days
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    prev_month_day = calendar.monthrange(prev_year, prev_month)[1]
    # check first week
    if 0 in cal[0]:
        # reverse week for easy input
        cal[0] = cal[0][::-1]
        for i, day in enumerate(cal[0]):
            if day == 0:
                cal[0][i] = prev_month_day
                prev_month_day -= 1
        # reverse back
        cal[0] = cal[0][::-1]

    # check last week
    if 0 in cal[-1]:
        next_day = 1
        for i, day in enumerate(cal[-1]):
            if day == 0:
                cal[-1][i] = next_day
                next_day += 1
    return cal
