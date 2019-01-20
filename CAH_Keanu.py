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

        # draw 100 posterior samples
        trace = sample(100, cores=1)
    return trace

def from_posterior(param, samples):
    smin, smax = np.min(samples), np.max(samples)
    width = smax - smin
    x = np.linspace(smin, smax, 100)
    y = stats.gaussian_kde(samples)(x)

    # what was never sampled should have a small probability but not 0,
    # so we'll extend the domain and use linear approximation of density on it
    x = np.concatenate([[x[0] - 3 * width], x, [x[-1] + 3 * width]])
    y = np.concatenate([[0], y, [0]])
    return Interpolated(param, x, y)

def Update_After_Win(Obs_Sent, X, N, Freq, trace):

    # Win Data = change in freqency distribution
    Obs_idx=np.argmin(abs(X-Obs_Sent))
    Freq[Obs_idx]=Freq[Obs_idx]+1

    #Normalisation
    Freq*N/(N+1)

    model = Model()
    with model:
        # Priors are posteriors from previous iteration
        alpha = from_posterior('alpha', trace['alpha'])
        beta = from_posterior('beta', trace['beta'])
        gamma = from_posterior('gamma', trace['gamma'])
        delta = from_posterior('delta', trace['delta'])
        #epsilon = from_posterior('epsilon', trace['epsilon'])

        Arg_A = np.linalg.norm(X-alpha)
        Arg_B = np.linalg.norm(X-beta)

        # Expected value of Frequency
        mu = gamma*np.exp(-2*Arg_A**2) + delta*np.exp(-2*Arg_B**2)

        # Likelihood (sampling distribution) of observations
        Y_obs = Normal('Y_obs', mu, 1, observed=Freq[Obs_idx])

        # draw 100 posterior samples
        trace = sample(100, cores=1)
    return(trace)


 #X=np.loadtxt('AWS_collapsed.txt')
# #X=np.loadtxt('az_score.txt')
 #X = (X+1)/2
# print(X)
# print(max(X),min(X))
# N=len(X)
# print(N)
# Freq=np.zeros(100)
# #
# for i in X:
#     Freq[int(np.ceil(i*100))]+=1
# #
# X=np.linspace(0,1,100)
# #
# trace=initialise_prior(X,Freq)
# mu_before = freq_expectation(X,trace)
# plt.plot(X,mu_before)
# #
# traceplot(trace)
# for i in range(0,10):
#     trace=Update_After_Win(0.5,X,N,Freq,trace)
# mu_after = freq_expectation(X,trace)
# plt.figure()
# plt.plot(X,mu_after)
# plt.show()

def plot_AI(X,trace):
    '''Plots the traceplot and modelled frequency distribution for the AI'''
    traceplot(trace)
    plt.figure()
    Y=freq_expectation(X,trace)
    plt.plot(X,trace)
    plt.show()
    return()
