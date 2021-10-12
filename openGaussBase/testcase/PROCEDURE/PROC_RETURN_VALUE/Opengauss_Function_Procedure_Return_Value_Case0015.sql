-- @testpoint: 测试存储过程返回值类型——char/varchar 合理报错

drop table if exists emp;
create table emp(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp values(1,'zhangsan','doctor1',10000),(2,'zhangsan2','doctor2',10000),(123,'zhangsan3','doctor3',10000);

--创建存储过程
create or replace procedure proc_return_value_015(p1 varchar)  as
v_char char(20);
begin
    v_char:=p1;
    raise info 'v_char=:%',v_char;
    exception
    when no_data_found
    then
    select * from emp;
    raise info 'no_data_found';
end;
/
--调用存储过程
declare
v1 varchar(200):='qwerttttyuioppppasdfg';
begin
proc_return_value_015(v1);
end;
/
--清理环境
drop procedure proc_return_value_015;
drop table emp;