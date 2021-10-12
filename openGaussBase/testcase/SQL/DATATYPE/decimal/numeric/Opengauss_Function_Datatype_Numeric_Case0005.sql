-- @testpoint: 插入精度小数点前边界范围值
-- @modified at: 2020-11-23

declare
  V_C text;
begin
  drop table if exists test_numeric_05;
  create table test_numeric_05 (name numeric);
  for i in 1 .. 131072 loop
    V_C := V_C || '9';
  end loop;
  V_C := V_C || '.1';
  insert into test_numeric_05 values (V_C);
end;
/
select char_length(name) from test_numeric_05;
drop table test_numeric_05;