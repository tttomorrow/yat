-- @testpoint: 存储过程中，select into语句中给int数据类型赋值，测试隐式数据类型转换

declare
  v_int int;
begin
    select 123456.7898765 into v_int from sys_dummy;
    raise info 'result: %',v_int;
end;
/


