import pandas as pd
import matplotlib.pyplot as plt


def clean_cov1(df, countries):
    # resolve conflicting country names
    country_names = countries.name.unique()
    problems = [c for c in df.Country.unique() if c not in country_names]
    for p in problems:
        p1 = p.split(', ')[0]
        results = [c for c in country_names if c.find(p1) > -1 or p1.find(c) > -1]
        df.loc[df.Country == p, 'Country'] = results[0] if len(results) > 0 else 'Korea, Republic of'

    # rename columns
    df = df.rename(columns={'Date': 'date',
                            'Country': 'country',
                            'Cumulative number of case(s)': 'total_confirmed',
                            'Number of deaths': 'total_deceased',
                            'Number recovered': 'total_recovered'})

    # add missing columns
    df.insert(5, 'total_tested', 'NaN')
    df.insert(6, 'new_confirmed', 'NaN')
    df.insert(7, 'new_deceased', 'NaN')
    df.insert(8, 'new_recovered', 'NaN')
    df.insert(9, 'new_tested', 'NaN')

    return df


def clean_cov2(df, countries):
    # ignore region data
    df = df[df.key.str.len() == 2]

    # set country names by joining the two dataframes
    countries = countries.rename(columns={'alpha-2': 'key'})
    df = df.merge(countries[['key', 'name']]).drop('key', axis=1)

    # rename column
    df = df.rename(columns={'name': 'country'})

    return df


def add_cov1_info(grouped, dataset):
    for g_idx, group in grouped:
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
                if row.total_confirmed < prev_row.total_confirmed:
                    row.total_confirmed = prev_row.total_confirmed
                    dataset.at[r_idx, 'total_confirmed'] = row.total_confirmed
                if row.total_deceased < prev_row.total_deceased:
                    row.total_deceased = prev_row.total_deceased
                    dataset.at[r_idx, 'total_deceased'] = row.total_deceased
                if row.total_recovered < prev_row.total_recovered:
                    row.total_recovered = prev_row.total_recovered
                    dataset.at[r_idx, 'total_recovered'] = row.total_recovered
                row.new_confirmed = row.total_confirmed - prev_row.total_confirmed
                row.new_deceased = row.total_deceased - prev_row.total_deceased
                row.new_recovered = row.total_recovered - prev_row.total_recovered
                dataset.at[r_idx, 'new_confirmed'] = row.total_confirmed - prev_row.total_confirmed
                dataset.at[r_idx, 'new_deceased'] = row.total_deceased - prev_row.total_deceased
                dataset.at[r_idx, 'new_recovered'] = row.total_recovered - prev_row.total_recovered
            prev_row = row
    return grouped


def plot_group(country):
    plt.figure()
    # plt.plot(country['date'], country['new_confirmed'])
    country.plot(x='date',
                 y=['total_confirmed', 'total_deceased', 'total_recovered'],
                 color=['r', 'k', 'g'],
                 xlabel='')
    plt.show()


def init_data():
    countries = pd.read_csv('datasets/countries.csv')
    df1 = pd.read_csv('datasets/COV-1.csv', parse_dates=['Date'])
    # df2 = pd.read_csv('datasets/COV-2.csv', parse_dates=['date'])

    df1 = clean_cov1(df1, countries)
    # df2 = clean_cov2(df2, countries)

    g1 = add_cov1_info(df1.groupby('country'), df1)
    # g2 = df2.groupby('country')

    return g1, None


if __name__ == "__main__":
    cov1, cov2 = init_data()
    # plot_group(cov2.get_group('China'))
    # print(cov2.get_group('China').head())
