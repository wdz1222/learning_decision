function fun = obj(x)
global k
global scp fcp
global dist
global mv_rating1 mv_rating2
global mv_scoring1 mv_scoring2
[m, ~] = size(mv_rating1);
fun = 0;
for i = 1 : m
    tp = meeting_prob(x(k+1), x(k+2), dist(i, 1));
    dp = decision_prob(x(1:k), x(k+3), mv_rating1(i, :), mv_scoring1(i, :), ...
        mv_rating2(i, :), mv_scoring2(i, :), dist(i, 2), k);
    fun = fun + scp*(log(tp)+log(dp)) + fcp*(log(tp)+log(1-dp));
end
fun = -fun;
