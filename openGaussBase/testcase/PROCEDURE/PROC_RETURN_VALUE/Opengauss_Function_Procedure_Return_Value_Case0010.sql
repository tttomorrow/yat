-- @testpoint: 测试存储过程返回值类型——int，且传入类型为boolean的情况

--创建存储过程
create or replace procedure proc_return_value_010(p1 in bool)  as
v_num int;
begin
    v_num:=p1;
    raise info 'v_num=:%',v_num;
    exception
    when no_data_found
    then raise info 'no_data_found';
end;
/
--调用存储过程
declare
    v1 bool:=true;
begin
    proc_return_value_010(v1);
end;
/
--调用存储过程
declare
    v2 bool:=false;
begin
    proc_return_value_010(v2);
end;
/
--清理环境
drop procedure proc_return_value_010;

