-- @testpoint: 测试存储过程返回值类型——real，溢出的情况 合理报错

--创建存储过程
create or replace procedure proc_return_value_018(p1 binary_double)  as
v_real real;
begin
    if(p1>=0)
    then
		v_real:=p1+0.0001;
       raise info 'v_real=:%',v_real;
    else
		v_real:=p1-0.0001;
        raise info 'v_real=:%',v_real;
    end if;
end;
/
--调用存储过程
declare
    v1 real:=-1.79e+308;
begin
    proc_return_value_018(v1);
end;
/
--调用存储过程
declare
    v2 real:=1.79e+308;
begin
    proc_return_value_018(v2);
end;
/
--清理环境
drop procedure proc_return_value_018;