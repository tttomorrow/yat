-- @testpoint: 测试select into语句中给bigint数据类型赋值，测试溢出int类型上边界，合理报错

declare
  v_bigint int8;
begin
    select 9223372036854775807.7898765 into v_bigint from sys_dummy;
    raise info 'result:% ',v_bigint;
end;
/
