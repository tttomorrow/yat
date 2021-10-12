-- @testpoint: 测试select into语句中给bigint数据类型赋值，测试溢出int类型上边界 合理报错

declare
  v_bigint bigint;
begin
    raise info 'result:% ',v_bigint;
end;
/
