-- @testpoint: 测试存储过程返回值类型——int 测试存储过程返回值类型——int，且溢出的情况 合理报错

drop table if exists table_003;
create table table_003(
  t1 int,
  t2 int,
  t3 bigint,
  t4 bigint,
  t5 number,
  t6 real,
  t7 decimal
) ;

create unique index  indx_t31 on table_003(t1);
create index indx_t32 on table_003(t2);

--创建存储过程
create or replace procedure proc_return_value_006  as
v1 int;
v8 int;
begin
    select t1 into v1 from table_003;
    v8:=v1+1;
    raise info 'v1=:%',v1;
    raise info 'v8=:%',v8;
    exception
    when no_data_found then raise info 'no_data_found';
end;
/
--调用存储过程
begin
    proc_return_value_006();
end;
/
--清理环境
drop procedure proc_return_value_006;
drop table table_003;