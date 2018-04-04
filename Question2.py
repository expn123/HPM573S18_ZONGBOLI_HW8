import numpy as np
import scipy.stats as stato
import scr.StatisticalClasses as Stat
import scr.FormatFunctions as Format


class Game:
    def __init__(self,id,p):
        self.id=id
        self.rnd=np.random
        self.rnd.seed(self.id)
        self.rarray = np.random.random(size=20)
        self.game_list = list(self.rarray)
        self.p=p
    def simulation(self):
        for k in range(0, 20):
            if self.rarray[k] > self.p:
                self.game_list[k] = 'H'
            else:
                self.game_list[k] = 'T'
        m = 0
        for j in range(0, len(self.game_list) - 2):
            if self.game_list[j] == 'T' and self.game_list[j + 1] == 'T' and self.game_list[j + 2] == 'H':
                m += 1
                j = j + 3
            else:
                m += 0
                j = j + 1
        total_result = 100 * m - 250
        return total_result

class Cohort:
    def __init__(self,id,pop_size,p):

        self.gamelist=[]
        self.catotal_score=[]
        self._sumSTAT=\
            Stat.SummaryStat('Gamblers total score', self.catotal_score)
        n=1
        self.p=p
        while n<=pop_size:
            gameunit=Game(id*pop_size+n,self.p)
            self.gamelist.append(gameunit)
            n+=1

    def simulatecohort(self):
        for game in self.gamelist:
            value=float(game.simulation())
            self.catotal_score.append(value)

    def get_expected_score(self):
        return sum(self.catotal_score)/len(self.catotal_score)

    def get_CI(self,alpha):
        return self._sumSTAT.get_t_CI(alpha)

class MultiCohort:
    def __init__(self,ids,pop_sizes,p):
        self._ids=ids
        self._popsizes=pop_sizes
        self._getallexprewards=[]
        self.p=p
    def simulate(self):
        for i in range(len(self._ids)):
            cohort=Cohort(i,self._popsizes,self.p)
            cohort.simulatecohort()
            self._getallexprewards.append(cohort.get_expected_score())

def print_comparative_outcomes(multi_cohort_high, multi_cohort_low):
    """ prints expected and percentage increase in average survival time when drug is available
    :param multi_cohort_no_drug: multiple cohorts simulated when drug is not available
    :param multi_cohort_with_drug: multiple cohorts simulated when drug is available
    """

    # increase in survival time
    increase = Stat.DifferenceStatIndp(
        name='Increase in mean game score',
        x=multi_cohort_high,
        y_ref=multi_cohort_low
    )
    # estimate and prediction interval
    estimate_CI = Format.format_estimate_interval(
        estimate=increase.get_mean(),
        interval=increase.get_PI(alpha=0.05),
        deci=1
    )
    print("Expected increase in mean game score of 10 games and {:.{prec}%} prediction interval:".format(1 -0.05, prec=0),
          estimate_CI)



testmultihigh=MultiCohort(range(1000),10,0.5)
testmultilow=MultiCohort(range(1000),10,0.55)
testmultihigh.simulate()
testmultilow.simulate()
scorehigh=testmultihigh._getallexprewards
scorelow=testmultilow._getallexprewards
print_comparative_outcomes(scorehigh,scorelow)
