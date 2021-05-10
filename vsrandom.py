from utils import *
from numpy.random import normal


class VaccineProgramme:
    def __init__(self, population=53_700_000, received_first=35_371_669,
                 received_second=17_669_379, dose_interval_days=76,
                 avg_daily_capacity=488_452, std_daily_capacity=132664.7):
        """
        Simulation of UK vaccine programme
        :param population: Total number of people that are eligible to be vaccinated
        :param received_first: Number of people that have already received a first dose of vaccine
        :param received_second: Number of people that have already received a second dose of vaccine
        :param daily_capacity: Total number of doses that can be given, daily
        :param dose_interval_days: Minimum interval between first and second dose (days)
        """
        self.population = population
        self.received_first = received_first
        self.received_second = received_second
        self.dose_interval_days = dose_interval_days

        self.day = None
        self.second_queue = None

        self.avg_daily_capacity = avg_daily_capacity
        self.std_daily_capacity = std_daily_capacity

    @property
    def daily_capacity(self):
        return normal(self.avg_daily_capacity, self.std_daily_capacity)

    def simulate_day(self):

        doses_left = self.daily_capacity

        # first do outstanding second doses
        for group in self.second_queue:

            people, due_day = group.no_people, group.value

            if due_day > self.day:
                break

            # do doses
            second_doses_given = min(people, doses_left)

            group.no_people -= second_doses_given
            doses_left -= second_doses_given

            self.received_second += second_doses_given

            if group.no_people == 0:
                self.second_queue.remove(group)
                continue

            if doses_left == 0:
                # ran out of doses
                break
        # end of second doses

        # then do first doses
        first_doses_given = min(self.population - self.received_second, doses_left)

        self.received_first += first_doses_given
        self.second_queue.append(GroupVar(first_doses_given, self.day + self.dose_interval_days))
        # end of first doses

    def run_simulation(self):

        self.day = 0
        self.second_queue = []  # stores list of lists, with element [due_day, number of people]

        # estimate distribution of second queue
        waiting_for_second = self.received_first - self.received_second

        # stores groups of people, each with value: second dose due day
        self.second_queue = [
            GroupVar(int(waiting_for_second / self.dose_interval_days), i)
            for i in range(self.dose_interval_days)
        ]

        while self.received_first < self.population:
            self.simulate_day()
            self.day += 1

        first_doses_done_on = self.day

        while self.received_second < self.population:
            self.simulate_day()
            self.day += 1

        second_doses_done_on = self.day

        return first_doses_done_on, second_doses_done_on


if __name__ == '__main__':
    vax = VaccineProgramme()
    first, second = vax.run_simulation()

    print(f"All first doses given by day {first}\nAll second doses given by day {second}")
