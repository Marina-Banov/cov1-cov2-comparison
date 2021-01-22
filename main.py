import csv
import pandas as pd


def load_dataset(file_name):
    ds = []
    with open(file_name, newline='') as f:
        next(f)
        reader = csv.reader(f)
        for row in reader:
            ds.append(row)
    return ds


def clean_us_data():
    d = load_dataset('datasets/us_deaths_csv.csv')
    c = load_dataset('datasets/us_confirmed_csv.csv')

    us_complete = [[], [], []]
    us_deaths = []
    us_cases = []

    for r_d, r_c in zip(d, c):
        if r_d[1] in us_complete[0]:
            us_deaths[us_complete[0].index(r_d[1])] += int(r_d[2])
            us_cases[us_complete[0].index(r_c[1])] += int(r_c[2])
        else:
            us_complete[0].append(r_d[1])
            us_deaths.append(0)
            us_cases.append(0)

    us_complete[1].extend(us_deaths)
    us_complete[2].extend(us_cases)

    print(us_complete[1])
    return


def clean_cov1(cov):
    cov = cov.rename(columns={'Date': 'date',
                              'Country': 'country',
                              'Cumulative number of case(s)': 'total_confirmed',
                              'Number of deaths': 'total_deceased',
                              'Number recovered': 'total_recovered'})
    cov.insert(5, 'total_tested', 'NaN')
    cov.insert(6, 'new_confirmed', 'NaN')
    cov.insert(7, 'new_deceased', 'NaN')
    cov.insert(8, 'new_recovered', 'NaN')
    cov.insert(9, 'new_tested', 'NaN')
    return cov


def clean_cov2(cov, countries):
    cov = cov.rename(columns={cov.columns[1]: 'country'})
    cov = cov[cov.country.str.len() == 2]
    cov['country'] = cov['country'].map(countries.set_index('key')['country_name'])
    return cov


def print_group(group):
    for state, frame in group:
        print(f"First 5 entries for {state!r}")
        print("------------------------")
        print(frame, end="\n\n")


def add_cov1_info(data_grouped_by_country, dataset):
    for g_idx, group in data_grouped_by_country:
        first = True
        prev_row = None
        for r_idx, row in group.iterrows():
            if first:
                row.new_confirmed = row.total_confirmed
                row.new_deceased = row.total_deceased
                row.new_recovered = row.total_recovered
                dataset.at[r_idx, 'new_confirmed'] = row.total_confirmed
                dataset.at[r_idx, 'new_deceased'] = row.total_deceased
                dataset.at[r_idx, 'new_recovered'] = row.total_recovered
                first = False
            else:
                row.new_confirmed = row.total_confirmed - prev_row.total_confirmed
                row.new_deceased = row.total_deceased - prev_row.total_deceased
                row.new_recovered = row.total_recovered - prev_row.total_recovered
                dataset.at[r_idx, 'new_confirmed'] = row.total_confirmed - prev_row.total_confirmed
                dataset.at[r_idx, 'new_deceased'] = row.total_deceased - prev_row.total_deceased
                dataset.at[r_idx, 'new_recovered'] = row.total_recovered - prev_row.total_recovered
            prev_row = row
    return data_grouped_by_country


def main():
    # countries = pd.read_csv('https://storage.googleapis.com/covid19-open-data/v2/index.csv')
    # cov2_dataset = pd.read_csv('https://storage.googleapis.com/covid19-open-data/v2/epidemiology.csv')
    countries = pd.read_csv('datasets/countries.csv')
    cov1_dataset = pd.read_csv('datasets/COV-1.csv')
    cov2_dataset = pd.read_csv('datasets/COV-2.csv')

    cov1_dataset = clean_cov1(cov1_dataset)
    cov2_dataset = clean_cov2(cov2_dataset, countries)

    groups_1 = add_cov1_info(cov1_dataset.groupby('country'), cov1_dataset)
    groups_2 = cov2_dataset.groupby('country')

    """
    cov1_dataset = load_dataset('datasets/COV-1-dataset.csv')
    cov2_dataset = load_dataset('datasets/COV-2-dataset.csv')
    
    clean_us_data()    

    countries = [Country(c) for c in list(set(row[1] for row in cov2_dataset))]
    pop = load_dataset('datasets/countries-population.csv')
    for row in pop:
        c = next((x for x in countries if x.name == row[0]), None)
        if c is not None:
            c.population_2003 = row[45]
            print(c)
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
        # print(e.cov)
        break

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
    """


if __name__ == "__main__":
    main()
