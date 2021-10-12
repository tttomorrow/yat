-- @testpoint: 插入超出精度小数点前边界范围长度值，合理报错

declare
  V_C text;
begin
  drop table if exists test_decimal_06;
  create table test_decimal_06 (name decimal);
  for i in 1 .. 131073 LOOP
    V_C := V_C || '9';
  end loop;
  insert into test_decimal_06 values (V_C || '0');
end;
/
