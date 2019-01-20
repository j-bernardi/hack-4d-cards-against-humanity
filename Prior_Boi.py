# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 15:27:12 2019

@author: user
"""


#matplotlib inline
import matplotlib.pyplot as plt
import matplotlib as mpl
import pymc3 as pm
from pymc3 import Model, Normal, Slice
from pymc3 import sample
from pymc3 import traceplot
from pymc3.distributions import Interpolated
from theano import as_op
import theano.tensor as tt
import numpy as np
from scipy import stats

def freq_expectation(X,trace):
    Arg_A = X-trace['alpha'].mean()
    Arg_B = X-trace['beta'].mean()
    mu = trace['gamma'].mean()*np.exp(-2*Arg_A**2) + trace['delta'].mean()*np.exp(-2*Arg_B**2)
    return mu


def initialise_prior(X, Freq):

    basic_model = Model()

    with basic_model:

        # Priors for unknown model parameters
        alpha = Normal('alpha', 0.5,0.5)
        beta = Normal('beta', 0.5,0.5)
        gamma = Normal('gamma',0.5,0.5)
        delta = Normal('delta',0.5,0.5)
        #epsilon = Uniform('epsilon',0,0.5)

        Arg_A = np.linalg.norm(X-alpha)
        Arg_B = np.linalg.norm(X-beta)

        # Expected value of Frequency
        mu = gamma*np.exp(-2*Arg_A**2) + delta*np.exp(-2*Arg_B**2)
        # Likelihood (sampling distribution) of observations
        Y_obs = Normal('Y_obs', mu, 1, observed=Freq)


        #saves to
        db = pm.backends.Text('AWS')
        trace = sample(100,cores=1,chains=1, trace=db)

        # draw 100 posterior samples
        # trace = sample(100, cores=1)

    return trace
X=np.loadtxt('AWS_collapsed.txt')
X = (X+1)/2

# N=len(X)
# print(N)
Freq=np.zeros(100)
# #
for i in X:
     Freq[int(np.ceil(i*100))]+=1

X=np.linspace(0,1,100)

trace=initialise_prior(X,Freq)
