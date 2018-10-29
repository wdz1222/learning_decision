function [dp] = decision_prob(v, alpha, r1, s1, r2, s2, d, k)
p1 = ranking_prob(r1, s1, v, k);
p2 = ranking_prob(r2, s2, v, k);
c = (1+d/2.3)^(-alpha);
dp = exp(p1*p2*c)/(1+exp(p1*p2*c));