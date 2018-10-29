function EM_learning()
global k
global scp fcp
global dist
global mv_rating1 mv_rating2
global mv_scoring1 mv_scoring2
dist = load('experiment3/4_dist.txt');
mv_rating1 = load('experiment3/4_mv_rating1.txt');
mv_rating2 = load('experiment3/4_mv_rating2.txt');
mv_scoring1 = load('experiment3/4_mv_scoring1.txt');
mv_scoring2 = load('experiment3/4_mv_scoring2.txt');
k = 4;
v = zeros(1, k) + 1/k;
a = 1;
b = 1;
alpha = 2;
[scp, fcp] = build_condi_prob(v, a, b, alpha);
Aeq = zeros(1, k+3);
Aeq(1:k) = 1;
beq = 1;
lb = zeros(1, k+3);
ub = zeros(1, k+3);
for i = 1 : k
    lb(i) = 0.01;
    ub(i) = 0.99;
end
lb(k+1) = 1; ub(k+1) = 5;
lb(k+2) = 1; ub(k+2) = 5;
lb(k+3) = 1; ub(k+3) = 10;
[x, feval] = ga(@obj, k+3, [], [], Aeq, beq, lb, ub)
x_new = zeros(1, k+3);
while norm(x-x_new) > 1e-3
    x_new = x;
    v = x(1:k);
    a = x(k+1);
    b = x(k+2);
    alpha = x(k+3);
    [scp, fcp] = build_condi_prob(v, a, b, alpha);
    [x, feval] = ga(@obj, k+3, [], [], Aeq, beq, lb, ub)
end


