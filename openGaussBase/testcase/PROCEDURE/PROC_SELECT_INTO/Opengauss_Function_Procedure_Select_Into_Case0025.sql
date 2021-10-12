-- @testpoint: 测试利用select into给指定精度和有效位的int数据类型赋值

declare
  v_sysdate number(12,2);
begin
    select 123456.7898765 into v_sysdate from sys_dummy;
    raise info 'result:% ',v_sysdate;
end;
/
