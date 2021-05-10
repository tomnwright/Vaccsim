import csv
from vsrandom import VaccineProgramme

csv_file = open("test output.csv", "w", newline="")

csv_writer = csv.writer(csv_file)

# title
csv_writer.writerow(["Test", "Day First Doses Done", "Day Second Doses Done"])

for i in range(1000):
    sim = VaccineProgramme()
    firsts, seconds = sim.run_simulation()

    csv_writer.writerow([i+1, firsts, seconds])






csv_file.close()