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


class GroupVar:
    def __init__(self, no_people, value, *args):
        self.no_people = no_people
        self.value = value  # day on which first dose was given

    def __repr__(self):
        return f"<{self.no_people} people : {self.value}>"


def average(iterable):
    return sum(iterable) / len(iterable)


def group_average(group_list):
    sum_vals = 0
    total_people = 0

    for _group in group_list:
        sum_vals += _group.no_people * _group.value
        total_people += _group.no_people

    return sum_vals / total_people


def total_groups_people(group_list):
    return sum(g.no_people for g in group_list)


cum_doses.reverse()

init_first, init_second = cum_doses[0]
waiting = init_first - init_second

second_dose_queue = [
    GroupVar(waiting, 0),  # value: day on which first dose given
]

intervals = []

output_file_name = "average_sim_output.csv"

csv_output = open(output_file_name, 'w', newline='')
csv_writer = csv.writer(csv_output)
csv_writer.writerow(
    ['Day', 'Cum. First Doses', 'Cum. Second Doses', 'New First Doses', 'New Second Doses', 'Second Dose Queue',
     'Total Second Doses Given'])
csv_writer.writerow(
        [0, cum_doses[0][0], cum_doses[0][1], "", "", total_groups_people(second_dose_queue),
         total_groups_people(intervals)])


for day in range(1, len(cum_doses)):

    new_first_doses = cum_doses[day][0] - cum_doses[day - 1][0]
    new_second_doses = cum_doses[day][1] - cum_doses[day - 1][1]
    print(new_second_doses)

    # register first doses
    second_dose_queue.append(
        GroupVar(new_first_doses, day)
    )

    # register second doses
    second_doses_remaining = new_second_doses

    for group in second_dose_queue:
        second_doses_given = min(group.no_people, second_doses_remaining)

        dose_interval = day - group.value

        # only count the last 30 days
        # if len(cum_doses) - day < include_past_days:

        intervals.append(GroupVar(second_doses_given, dose_interval))

        group.no_people -= second_doses_given
        second_doses_remaining -= second_doses_given

        if group.no_people == 0:
            second_dose_queue.remove(group)

        if second_doses_remaining == 0:
            break
    csv_writer.writerow(
        [day, cum_doses[day][0], cum_doses[day][1], new_first_doses, new_second_doses, total_groups_people(second_dose_queue),
         total_groups_people(intervals)])

csv_output.close()

print(group_average(intervals))
print(f"Total people given second dose: {total_groups_people(intervals)}")

print("\nThese people are still waiting to be vaccinated right now:")
print(second_dose_queue)
