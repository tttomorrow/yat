-- @testpoint: 测试存储过程返回值类型——日期类型，date/timestamp和char类型的互相转化

drop table if exists table_009;
create table table_009(
  t1 date,
  t2 char(400),
  t3 timestamp,
  t4 varchar(1000)
) ;

create unique index  indx_t91 on table_009(t1);
create index indx_t92 on table_009(t2);
insert into table_009 values (to_date('0001-01-01 00:00:00','yyyy-mm-dd hh24:mi:ss'),'9999-12-31 23:59:59',
to_timestamp('0001-01-01 00:00:00.000000','yyyy-mm-dd hh24:mi:ss.ffffff'),'9999-12-31 23:59:59.999999');

--创建存储过程
create or replace procedure proc_return_value_023  as
v1 char(400);
v2 date;
v3 varchar(1000);
v4 timestamp;
begin
    select to_char(t1,'yyyy-mon-dd hh:mi:ss') into v1 from table_009;
    select to_date(t2,'yyyy-mm-dd hh24:mi:ss') into v2 from table_009;
    select to_char(t3,'yyyy-mm-dd hh24:mi:ss.ffffff') into v3 from table_009;
    select to_date(t4,'yyyy-mm-dd hh24:mi:ss.ff') into v4 from table_009;
    raise info 'v1=:%',v1;
    raise info 'v2=:%',v2;
    raise info 'v3=:%',v3;
    raise info 'v4=:%',v4;
    exception
    when no_data_found
    then raise info 'no_data_found';
end;
/
--调用存储过程
call proc_return_value_023();
--清理环境
drop procedure proc_return_value_023;
drop table table_009;