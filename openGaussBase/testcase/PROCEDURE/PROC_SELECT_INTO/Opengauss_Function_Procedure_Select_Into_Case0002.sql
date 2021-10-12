-- @testpoint: 匿名块中,select into语句中给int数据类型赋值，测试溢出int类型上边界 合理报错

declare
  v_int int;
begin
    raise info 'result:% ',v_int;
end;
/
