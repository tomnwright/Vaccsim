population = 53_700_000
received_first = 35_371_669
received_second = 17_669_379

daily_capacity = 500_000  # daily dosage capacity
dose_interval_days = 76


def simulate_day():
    global received_first
    global received_second
    global second_queue

    doses_left = daily_capacity

    # first do outstanding second doses
    for e, q in enumerate(second_queue):
        due_day, people = q

        if due_day > day:
            break

        # do doses
        second_doses_given = min(people, doses_left)

        people -= second_doses_given
        doses_left -= second_doses_given

        received_second += second_doses_given

        if people == 0:
            del second_queue[e]
            continue

        # then doses_left=0 - we ran out of doses

        second_queue[e][1] = people
        break
    # end of second doses

    # then do first doses
    first_doses_given = min(population-received_second, doses_left)

    received_first += first_doses_given
    second_queue.append([day + dose_interval_days, first_doses_given])
    # end of first doses


day = 0
second_queue = []  # stores list of lists, with element [due_day, number of people]

# estimate distribution of second queue
wait_second = received_first - received_second

for i in range(dose_interval_days):
    second_queue.append([i, int(wait_second / dose_interval_days)])

while received_first < population:
    simulate_day()
    day += 1

print(f"First doses given after {day} days")

while received_second < population:
    simulate_day()
    day += 1

print(f"Second doses given after {day} days")
