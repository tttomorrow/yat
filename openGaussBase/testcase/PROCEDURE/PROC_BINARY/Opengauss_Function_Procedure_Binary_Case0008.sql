-- @testpoint: 存储过程结合二进制类型的测试 raw类型转换为char/varchar类型

drop table if exists proc_binary_table_008;
create table proc_binary_table_008(t1 int,t2 raw(100));
insert into proc_binary_table_008 values(1,'01affb6710114657895500101');

--创建存储过程
create or replace procedure proc_binary_008() is
v1 char(100);
v2 varchar(100);
begin
    select t2 into v1 from proc_binary_table_008 where t1=1;
    raise info 'v1=:%',v1;
    select t2 into v2 from proc_binary_table_008 where t1=1;
    raise info 'v2=:%',v2;
    exception
    when no_data_found then
        raise info 'no_data_found';
end;
/

--调用存储过程
call proc_binary_008();

--恢复环境
drop table if exists proc_binary_table_008;
drop procedure if exists proc_binary_008;

