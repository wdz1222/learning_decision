function [mp] = meeting_prob(a, b, v)
mp = exp(b*v)/(a+exp(b*v));