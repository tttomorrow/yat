-- @testpoint: 测试select into语句中给bigint数据类型赋值，测试通过指数赋值

declare
  v_real real;
begin
    select 3e+2 into v_real from sys_dummy;
    raise info 'result:% ',v_real;
end;
/
