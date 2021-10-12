-- @testpoint: 测试存储过程返回值类型——char/varchar类型

drop table if exists table_005;
create table table_005(
  t1 char(100),
  t2 char(20),
  t3 varchar(4000),
  t4 varchar(4000),
  t5 char(100),
  t6 varchar(400),
  t7 char(1000)
) ;

create unique index  indx_t51 on table_005(t1);
create index indx_t52 on table_005(t2);
insert into table_005 values('asdfghjklzxcvb','qwertzxcvbzxcvbnmqwe','这是一个变长的字符串，最大字节支持4000。','gfytfcogdub','',' ','ajdg127_$%./煤球');

create or replace procedure proc_return_value_014  as
v1 char(8000);
v2 char(20);
v3 varchar(6000);
v4 char(100);
v5 char(100);
v6 varchar2(100);
v7 char(1000);
begin
    select t1 into v1 from table_005;
    select t2 into v2 from table_005;
    select t3 into v3 from table_005;
    select t4 into v4 from table_005;
    select t5 into v5 from table_005;
    select t6 into v6 from table_005;
    select t7 into v7 from table_005;
    raise info 'v1=:%',v1;
    raise info'v2=:%',v2;
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
begin
 proc_return_value_014();
end;
/
--清理环境
drop procedure proc_return_value_014;
drop table table_005;