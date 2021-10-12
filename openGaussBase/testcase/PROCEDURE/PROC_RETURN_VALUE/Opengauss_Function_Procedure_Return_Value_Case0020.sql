-- @testpoint: 测试存储过程返回值类型——number/decimal，溢出的情况

--创建存储过程
create or replace procedure proc_return_value_020(p1 decimal)  as
v_dec number;
begin
v_dec:=p1;
raise info 'v_dec=:%',v_dec;
exception
when no_data_found then raise info 'no_data_found';
end;
/
--调用存储过程
declare
    v1 number:=-1.0e128;
begin
    proc_return_value_020(v1);
end;
/
--调用存储过程
declare
    v2 number:=1.0e128;
begin
    proc_return_value_020(v2);
end;
/
--清理环境
drop procedure proc_return_value_020;