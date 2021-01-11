class Country:
    def __init__(self, name):
        self.name = name
        self.cov1 = Pandemic('COV-1')
        self.cov2 = Pandemic('COV-2')
        self.population_2003 = 0
        self.population_2020 = 0

    def __repr__(self):
        return self.name


class Pandemic:
    def __init__(self, name):
        self.name = name
        self.dates = []

    def calc_daily_cases(self):
        if len(self.dates) == 1:
            self.dates[0].daily_cases = self.dates[0].cumulative_cases
        else:
            self.dates[-1].daily_cases = self.dates[-1].cumulative_cases - self.dates[-2].cumulative_cases

    def calc_daily_deaths(self):
        if len(self.dates) == 1:
            self.dates[0].daily_deaths = self.dates[0].cumulative_deaths
        else:
            self.dates[-1].daily_deaths = self.dates[-1].cumulative_deaths - self.dates[-2].cumulative_deaths

    def calc_daily_recovered(self):
        if len(self.dates) == 1:
            self.dates[0].daily_recovered = self.dates[0].cumulative_recovered
        else:
            self.dates[-1].daily_recovered = self.dates[-1].cumulative_recovered - self.dates[-2].cumulative_recovered

    def calc_cum_deaths(self):
        if len(self.dates) == 1:
            self.dates[0].cumulative_deaths = self.dates[0].daily_deaths
        else:
            self.dates[-1].cumulative_deaths = self.dates[-2].cumulative_deaths + self.dates[-1].daily_deaths

    def calc_cum_recovered(self):
        if len(self.dates) == 1:
            self.dates[0].cumulative_recovered = self.dates[0].daily_recovered
        else:
            self.dates[-1].cumulative_recovered = self.dates[-2].cumulative_recovered + self.dates[-1].daily_recovered

    def __repr__(self):
        return self.name


class PandemicEntry:
    def __init__(self, date):
        self.date = date
        self.cumulative_cases = 0
        self.cumulative_deaths = 0
        self.cumulative_recovered = 0
        self.daily_cases = 0
        self.daily_deaths = 0
        self.daily_recovered = 0
