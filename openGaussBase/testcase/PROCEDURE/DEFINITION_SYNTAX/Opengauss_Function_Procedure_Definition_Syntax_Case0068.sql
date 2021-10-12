-- @testpoint: 测试select into语句中给bigint数据类型赋值，测试通过指数赋值下边界值，合理报错

declare
  v_real real;
begin
    raise info 'result:% ',v_real;
end;
/


