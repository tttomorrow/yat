-- @testpoint: 测试select into语句中给int数据类型赋值，测试real隐式转换为number下界内边缘 合理报错

declare
   v_real real;
   v_number number(12,3);
begin
    select v_real into v_number from sys_dummy;
    raise info 'result:% ',v_number;
end;
/
