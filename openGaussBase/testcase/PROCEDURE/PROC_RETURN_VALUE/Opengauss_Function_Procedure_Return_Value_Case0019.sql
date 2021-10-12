-- @testpoint: 测试存储过程返回值类型——number/decimal,能正常返回的number/decimal类型

drop table if exists table_007;
create table table_007(
  t1 number,
  t2 decimal,
  t3 numeric,
  t4 number,
  t5 decimal,
  t6 number(16,9),
  t7 number(16,3)
) ;

create unique index  indx_t71 on table_007(t1);
create index indx_t72 on table_007(t2);
insert into table_007 values(0.000000,-9.9999999e127,9.99999999e127,-0.9e127,1.79e123,999999.999999,-123456.789);

--创建存储过程
create or replace procedure proc_return_value_019  as
v1 decimal;
v2 number;
v3 numeric;
v4 number;
v5 decimal;
v6 number(12,6);
v7 number(9,2);
begin
    select t1 into v1 from table_007;
    select t2 into v2 from table_007;
    select t3 into v3 from table_007;
    select t4 into v4 from table_007;
    select t5 into v5 from table_007;
    select t6 into v6 from table_007;
    select t7 into v7 from table_007;
    raise info 'v1=:%',v1;
    raise info 'v2=:%',v2;
    raise info 'v3=:%',v3;
    raise info 'v4=:%',v4;
    raise info 'v5=:%',v5;
    raise info 'v6=:%',v6;
    raise info 'v7=:%',v7;
    exception
    when no_data_found
    then raise info 'no_data_found';
end;
/

--调用存储过程
call proc_return_value_019();
--清理环境
drop procedure proc_return_value_019;
drop table table_007;