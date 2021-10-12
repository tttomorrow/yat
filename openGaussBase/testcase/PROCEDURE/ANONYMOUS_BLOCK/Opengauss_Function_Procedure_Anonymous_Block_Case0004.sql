-- @testpoint: 验证匿名块内变量是否区分大小写

declare
  v_real real;
begin
    select 7.7898765+1 into v_real from sys_dummy;
    raise info 'result:% ',v_real;
end;
/