from utils import *
import csv

include_past_days = 30

# READ DATA

cum_doses = []  # cumulative doses given - first and second

with open("data/data_2021-May-09.csv", newline="") as csv_file:
    reader = csv.reader(csv_file, delimiter=',', quotechar='|')

    for row in reader:
        try:
            cum_first, cum_second = int(row[7]), int(row[9])
        except ValueError:
            # not a number
            continue
        else:
            cum_doses.append((cum_first, cum_second))


cum_doses.reverse()

init_first, init_second = cum_doses[0]
waiting = init_first - init_second

second_dose_queue = [
    GroupVar(waiting, 0),  # value: day on which first dose given
]

intervals = []  # list of groups, each with a dose interval value

for day in range(1, len(cum_doses)):

    new_first_doses = cum_doses[day][0] - cum_doses[day - 1][0]
    new_second_doses = cum_doses[day][1] - cum_doses[day - 1][1]

    # register first doses
    second_dose_queue.append(
        GroupVar(new_first_doses, day)
    )

    # register second doses
    second_doses_remaining = new_second_doses

    for group in second_dose_queue:
        second_doses_given = min(group.no_people, second_doses_remaining)

        dose_interval = day - group.value

        # only count the last [include_past_days] days in average
        if len(cum_doses) - day <= include_past_days:
            intervals.append(GroupVar(second_doses_given, dose_interval))

        group.no_people -= second_doses_given
        second_doses_remaining -= second_doses_given

        if group.no_people == 0:
            second_dose_queue.remove(group)

        if second_doses_remaining == 0:
            break

# note, total_groups_people(intervals) DOES NOT measure total number of second doses given

print(f"Average dose interval in past {include_past_days} days: {round(group_average(intervals),1)} days.")
