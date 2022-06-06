-- @testpoint: select into语句中给int数据类型赋值，截取到int类型下边界 合理报错

declare
  v_int int;
begin
    select -2147483648.7898765 into v_int from sys_dummy;
     raise info 'result:% ',v_int;
end;
/
