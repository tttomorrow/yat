-- @testpoint: 测试select into语句中带有简单数学表达式时给int数据类型赋值

declare
  v_real real;
begin
    select 7.7898765+1 into v_real from sys_dummy;
    raise info 'result:% ',v_real;
end;
/
