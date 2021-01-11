import csv
from classes import Country, PandemicEntry


def load_dataset(file_name):
    ds = []
    with open(file_name, newline='') as f:
        next(f)
        reader = csv.reader(f)
        for row in reader:
            ds.append(row)
    return ds


def main():
    cov1_dataset = load_dataset('COV-1-dataset.csv')
    cov2_dataset = load_dataset('COV-2-dataset.csv')

    countries = [Country(c) for c in list(set(row[1] for row in cov2_dataset))]
    pop = load_dataset('countries-population.csv')
    for row in pop:
        c = next((x for x in countries if x.name == row[0]), None)
        if c is not None:
            c.population_2003 = row[45]
            # TODO prepare a better csv with world population
    del pop

    for row in cov1_dataset:
        e = PandemicEntry(row[0])
        e.cumulative_cases = int(row[2])
        e.daily_deaths = int(row[3])
        e.daily_recovered = int(row[4])
        c = next((x for x in countries if x.name == row[1]), None)
        if c is None:
            print(row[1])
        else:
            c.cov1.dates.append(e)
            c.cov1.calc_daily_cases()
            c.cov1.calc_cum_deaths()
            c.cov1.calc_cum_recovered()

    for row in cov2_dataset:
        e = PandemicEntry(row[0])
        e.cumulative_cases = int(row[2])
        e.cumulative_recovered = int(row[3])
        e.cumulative_deaths = int(row[4])
        c = next((x for x in countries if x.name == row[1]), None)
        c.cov2.dates.append(e)
        c.cov2.calc_daily_cases()
        c.cov2.calc_daily_deaths()
        c.cov2.calc_daily_recovered()


if __name__ == "__main__":
    main()
