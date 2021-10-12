-- @testpoint: 存储过程结合blob数据类型的测试，存储过程内的blob类型和raw类型的转换

drop table if exists proc_blob_table_002;
create table proc_blob_table_002(t1 int,t2 blob);

--创建存储过程
create or replace procedure proc_blob_002(v1 out raw) is
begin
    select t2 into v1 from proc_blob_table_002 where t1=1;
        raise info 'v1=:%',v1;
        raise info 'length=:%',length(v1);
    exception
    when no_data_found then
        raise info 'no_data_found';
end;
/
--调用存储过程
call proc_blob_002('100');

--恢复环境
drop procedure if exists proc_blob_002;
drop table proc_blob_table_002;

