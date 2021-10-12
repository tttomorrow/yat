-- @testpoint: 存储过程结合二进制类型的测试 测试raw类型为null

drop table if exists proc_binary_table_002;
create table proc_binary_table_002(t1 int,t2 raw(100));
insert into proc_binary_table_002 values(1,'');

--创建存储过程
create or replace procedure proc_binary_002() is
v1 raw(100);
begin
    select t2 into v1 from proc_binary_table_002 where t1=1;
    raise info 'v1=:%',v1;
    raise info 'length=:%',length(v1);
    exception
    when no_data_found then
        raise info 'no_data_found';
end;
/

--调用存储过程
call proc_binary_002();

--恢复环境
drop table if exists proc_binary_table_002;
drop procedure if exists proc_binary_002;

