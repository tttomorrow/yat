-- @testpoint: 测试存储过程返回值类型——bigint，能正常返回的int、bigint、real类型

drop table if exists table_004;
create table table_004(
  t1 bigint,
  t2 bigint not null,
  t3 bigint,
  t4 int,
  t5 int,
  t6 bigint,
  t7 number,
  t8 number
) ;

create unique index  indx_t41 on table_004(t1);
create index indx_t42 on table_004(t2);
insert into table_004 values(0,-9223372036854775808,9223372036854775807,-2147483648,2147483647,21474836469065,9223372036854775807.00,-0.001);

--创建存储过程
create or replace procedure proc_return_value_011  as
v1 bigint;
v2 bigint;
v3 bigint;
v4 bigint;
v5 bigint;
v6 bigint;
v7 bigint;
v8 bigint;
begin
    select t1 into v1 from table_004;
    select t2 into v2 from table_004;
    select t3 into v3 from table_004;
    select t4 into v4 from table_004;
    select t5 into v5 from table_004;
    select t6 into v6 from table_004;
    select t7 into v7 from table_004;
    select t8 into v8 from table_004;
    raise info 'v1=:%',v1;
    raise info 'v2=:%',v2;
    raise info 'v3=:%',v3;
    raise info 'v4=:%',v4;
    raise info 'v5=:%',v5;
    raise info 'v6=:%',v6;
    raise info 'v7=:%',v7;
    raise info 'v8=:%',v8;
    exception
    when no_data_found then
    raise info 'no_data_found';
end;
/
--调用存储过程
begin
    proc_return_value_011();
end;
/
--清理环境
drop procedure proc_return_value_011;
drop table table_004;