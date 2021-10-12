-- @testpoint: 测试无参的存储过程的返回值

drop table if exists table_001;
create table table_001(
  t1 int,
  t2 integer not null,
  t3 bigint,
  t4 number default 0.2332,
  t5 number(12,2),
  t6 number(12,6),
  t7 binary_double,
  t8 decimal,
  t9 decimal(8,2),
  t10 decimal(8,4),
  t11 real,
  t12 char(4000),
  t13 char(100),
  t14 varchar(4000),
  t15 varchar(100),
  t16 varchar2(4000),
  t17 numeric,
  t19 date,
  t20 timestamp,
  t21 timestamp(6),
  t22 bool
) ;


--创建存储过程
create or replace procedure proc_return_value_001 as
v_count integer;
begin
    select count(*) into v_count from table_001 where t22=true;
    raise info 'v_count:%',v_count;
    exception
    when no_data_found
    then raise info 'no_data_found';
end;
/
--调用存储过程
call proc_return_value_001();
--清理环境
drop procedure proc_return_value_001;
drop table table_001;