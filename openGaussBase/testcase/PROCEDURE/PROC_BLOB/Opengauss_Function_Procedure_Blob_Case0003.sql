-- @testpoint: 存储过程结合blob数据类型的测试

drop table if exists proc_blob_table_003;
create table proc_blob_table_003(t1 int,t2 blob);
insert into proc_blob_table_003 values(1*9,hextoraw('deadbeef'));

--创建存储过程
create or replace procedure proc_blob_003() is
v1 blob;
begin
    select t2 into v1 from proc_blob_table_003 where t1=1;
        raise info 'v1=:%',v1;
        raise info 'length=:%',v1;
    exception
    when no_data_found then
        raise info 'no_data_found';
end;
/
--调用存储过程
call proc_blob_003();

--恢复环境
drop procedure if exists proc_blob_003;
drop table proc_blob_table_003;
