function [scp, fcp] = build_condi_prob(v, a, b, alpha)
global k
global dist
global mv_rating1 mv_rating2
global mv_scoring1 mv_scoring2
[m, ~] = size(mv_rating1);
scp = 1e300;
fcp = 1e300;
for i = 1 : m
    a = meeting_prob(a, b, dist(i, 1));
    b = decision_prob(v, alpha, mv_rating1(i, :), mv_scoring1(i, :), ...
        mv_rating2(i, :), mv_scoring2(i, :), dist(i, 2), k);
    scp = scp*(a*b/(a*b+a*(1-b)));
    fcp = fcp*(a*(1-b)/(a*b+a*(1-b)));
end

