-- @testpoint: 存储过程中,select into语句中给int数据类型赋值，测试溢出int类型上边界，合理报错

declare
  v_int INT4;
begin
    select 2147483647.7898765 into v_int from sys_dummy;
    raise info 'result:% ',v_int;
end;
/
