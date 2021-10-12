-- @testpoint: 插入超出精度小数点后边界范围值，合理报错
-- @modified at: 2020-11-23

declare
  V_C text;
begin
  V_C :='2.9';
  drop table if exists test_decimal_07;
  create table test_decimal_07 (name decimal);
  for i in 1 .. 16384 loop
    V_C := V_C || '9';
  end loop;
  insert into test_decimal_07 values (V_C);
end;
/
