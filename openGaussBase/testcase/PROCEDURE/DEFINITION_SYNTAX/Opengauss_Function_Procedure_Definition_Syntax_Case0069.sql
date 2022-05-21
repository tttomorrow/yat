-- @testpoint: 测试select into语句中给int数据类型赋值，测试real隐式转换为int，合理报错

declare
   v_real real;
   v_int int;
begin
    v_real:=2147483646.7898765;
    select v_real into v_int from sys_dummy;
    raise info 'result:% ',v_int;
end;
/

