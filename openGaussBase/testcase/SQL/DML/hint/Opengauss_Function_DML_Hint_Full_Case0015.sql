-- @testpoint:同一个查询语句分别走full、index路线查询
 select fint1, fint2, fstr1, fstr2 from t_hint where fint1=1;
 select /*+ FULL(t) */ fint1, fint2, fstr1, fstr2 from t_hint t where fint1=1;
 select /*+ index(t,t_hint_idx2) */ fint1, fint2, fstr1, fstr2 from t_hint t where fint1 = 1;