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

def print_comparative_outcomes(sim_output_high, sim_output_low):

    # increase in survival time
    increase = Stat.DifferenceStatIndp(
        name='Increase in game score',
        x=sim_output_high,
        y_ref=sim_output_low
    )
    # estimate and CI
    estimate_CI = Format.format_estimate_interval(
        estimate=increase.get_mean(),
        interval=increase.get_t_CI(alpha=0.05),
        deci=1
    )
    print("Average increase in game score and {:.{prec}%} confidence interval:".format(1 - 0.05, prec=0),
          estimate_CI)

    # % increase in survival time
    relative_diff = Stat.RelativeDifferenceIndp(
        name='Average % increase in game score',
        x=sim_output_high,
        y_ref=sim_output_low
    )
    # estimate and CI
    estimate_CI = Format.format_estimate_interval(
        estimate=relative_diff.get_mean(),
        interval=relative_diff.get_bootstrap_CI(alpha=0.05, num_samples=1000),
        deci=1,
        form=Format.FormatNumber.PERCENTAGE
    )
    print("Average percentage increase in game score and {:.{prec}%} confidence interval:".format(1 - 0.05, prec=0),
          estimate_CI)

testcohorthigh=Cohort(1,1000,0.5)
testcohortlow=Cohort(1,1000,0.55)
testcohorthigh.simulatecohort()
testcohortlow.simulatecohort()
scorehigh=testcohorthigh.catotal_score
scorelow=testcohortlow.catotal_score
print_comparative_outcomes(scorehigh,scorelow)
