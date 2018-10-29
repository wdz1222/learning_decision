function [p] = ranking_prob(r, s, v, k)
if sum(s) == 0
    p = prod(v)/sum(v).^k;
else
    vt = v;
    pt = zeros(1, k);
    pt(1) = v(r(1))/sum(v);
    vt(r(1)) = 0;
    for j = 2 : k
        if s(j) == s(j-1)
            pt(j) = pt(j-1);
        else
            pt(j) = v(r(j))/sum(vt);
        end
        vt(r(j)) = 0;
    end
    p = prod(pt);
end