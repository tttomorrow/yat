-- @testpoint: 测试含in参数的存储过程返回值

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

insert into table_001 values(12,58812,546223079,1234567.89,12345.6789,12.3456789,1234.56,2345.67,12345.6789,12.3456789,12.33,'dbcd','abcde','1999-01-01','ab','adc',123.45,'2005-08-08','2000-01-01 15:12:21.11','2000-08-01 15:12:21.32',true);
insert into table_001 values(13,58813,546223078,1234567.78,12345.5678,12.2345678,1234.67,2345.78,12345.5678,12.2345678,12.44,'dbce','abcdf','abcdeg','ac','ade',123.46,'2012-08-08','2000-02-01 15:22:21.11','2012-02-01 15:12:11.32',false);
insert into table_001 values(14,58814,546223077,1234567.67,12345.4567,12.1234567,1234.78,2345.89,12345.4567,12.1234567,12.55,'dbcf','abcdg','2010-02-28','ad','adf',123.47,'2002-08-11','2000-03-01 15:42:21.11','2008-08-12 15:13:21.32',true);
insert into table_001 values(15,58814,546223077,1234567.67,12345.4567,12.1234567,1234.78,2345.89,12345.4567,12.1234567,12.55,'dbcf','abcdg','abcdeh','ad','adf',123.47,'2002-08-11','2000-03-01 15:42:21.11','2008-08-12 15:13:21.32',true);
insert into table_001 values(16,58814,546223077,1234567.67,12345.4567,12.1234567,1234.78,2345.89,12345.4567,12.1234567,12.55,'dbcf','abcdg','abcdeh','ad','adf',123.47,'2002-08-11','2000-03-01 15:42:21.11','2008-08-12 15:13:21.32',true);

--创建存储过程
create or replace procedure proc_return_value_002(p1 in int default 1,p2 varchar) as
v1 int;
v2 char(100);
begin
    select t2 into v1 from table_001 where t1=p1;
    select t13 into v2 from table_001 where t14=p2;
    raise info 'p1:%',p1;
    raise info 'p2:%',p2;
    raise info 'v1:%',v1;
    raise info 'v2:%',v2;
    exception
    when no_data_found
    then raise info 'no_data_found';
end;
/
--调用存储过程
begin
    proc_return_value_002(p1=>12,p2=>'abcdeg');
end;
/
--清理环境
drop procedure proc_return_value_002;
drop table table_001;