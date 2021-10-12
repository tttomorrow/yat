-- @testpoint:full里面带表名和索引名，计划无效
  select fint1, fint2, fstr1, fstr2 from t_hint where fint1=1;
  select /*+ FULL(t) */ fint1, fint2, fstr1, fstr2 from t_hint t where fint1=1;
  select /*+ FULL(t t_hint_idx2) */ fint1, fint2, fstr1, fstr2 from t_hint t where fint1=1;
  select /*+ FULL(t_hint_idx2) */ fint1, fint2, fstr1, fstr2 from t_hint t where fint1=1;