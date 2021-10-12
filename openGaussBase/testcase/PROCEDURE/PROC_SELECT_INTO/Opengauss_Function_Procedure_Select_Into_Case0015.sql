-- @testpoint: 测试select into语句中给bigint数据类型赋值，测试溢出int类型下边界 合理报错

declare
  v_int int;
begin
    raise info 'result:%',v_int;
end;
/
