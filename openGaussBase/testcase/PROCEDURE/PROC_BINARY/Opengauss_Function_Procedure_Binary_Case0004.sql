-- @testpoint: 存储过程二进制类型的测试 测试raw类型和blob的转换

drop table if exists proc_binary_table_004;
create table proc_binary_table_004(t1 int,t2 raw(100));
insert into proc_binary_table_004 values(1,'01fabd011365489000');

--创建存储过程
create or replace procedure proc_binary_004() is
v1 proc_binary_table_004.t2%type;
begin
    select t2 into v1 from proc_binary_table_004 where t1=1;
    raise info'v1=:%',v1;
    raise info 'length=:%',length(v1);
    exception
when no_data_found then
    raise info 'no_data_found';
end;
/
--调用存储过程
call proc_binary_004();

--向表中增加新列
alter table proc_binary_table_004 add t3 raw(100);
select * from proc_binary_table_004;

--更新表中数据
update proc_binary_table_004 set t3=t2 ,t2=null;
select * from proc_binary_table_004;

--调用存储过程
call proc_binary_004();

--将表中t2列raw属性修改为blob属性
alter table proc_binary_table_004 modify t2 blob;

--更新表中数据
update proc_binary_table_004 set t2=t3 where t3 is not null;
select * from proc_binary_table_004;

--删除表中t3lie
alter table proc_binary_table_004 drop column t3;
select * from proc_binary_table_004;

--清理环境
drop table if exists proc_binary_table_004;
drop procedure if exists proc_binary_004;

