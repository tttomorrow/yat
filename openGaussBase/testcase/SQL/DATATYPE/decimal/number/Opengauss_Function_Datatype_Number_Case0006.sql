-- @testpoint: 插入超出精度小数点前边界范围值，合理报错
-- @modified at: 2020-11-23

declare
  V_C text;
begin
  drop table if exists test_number_06;
  create table test_number_06 (name number);
  for i in 1 .. 131073 loop
    V_C := V_C || '9';
  end loop;
  insert into test_number_06 values (V_C || '0');
end;
/
