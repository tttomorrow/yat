-- @testpoint: 测试存储过程返回值类型——日期类型 date/timestamp输出时长度溢出的情况 会四舍五入，不报错

drop table if exists table_010;
create table table_010(
  t1 varchar(1000)
) ;
insert into table_010 values ('9999-12-31 23:59:59.586');
--创建存储过程
create or replace procedure proc_return_value_024  as
v1 timestamp(2); 
begin
    select to_date(t1,'yyyy-mm-dd hh24:mi:ss.ff') into v1 from table_010;
    raise info 'v1=:%',v1;
    exception
    when no_data_found
    then raise info 'no_data_found';
end;
/
--调用存储过程
call proc_return_value_024();
--清理环境
drop procedure proc_return_value_024;
drop table table_010;
