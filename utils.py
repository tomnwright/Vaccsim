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
