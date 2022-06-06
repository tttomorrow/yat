-- @testpoint: 测试存储过程返回值类型——int

--创建存储过程
create or replace procedure proc_return_value_008(p1 in bigint)  as
v_num int;
begin
    v_num:=p1;
    raise info 'v_num=:%',v_num;
    exception
    when no_data_found
    then raise info 'no_data_found%';
end;
/
--调用存储过程
declare
    v1 integer:=123456789;
begin
    proc_return_value_008(v1);
end;
/
--调用存储过程
declare
    v2 integer:=-21474836;
begin
    proc_return_value_008(v2);
end;
/
--清理环境
drop procedure proc_return_value_008;