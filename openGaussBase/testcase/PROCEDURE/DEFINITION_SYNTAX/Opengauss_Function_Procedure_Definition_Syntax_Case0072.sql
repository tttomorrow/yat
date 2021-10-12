-- @testpoint: 定义匿名块，不加/结尾，合理报错

declare
  v_sysdate number(16,10);
begin
    select 123456.7898765 into v_sysdate from sys_dummy;
    raise info 'result:% ',v_sysdate;
end;

