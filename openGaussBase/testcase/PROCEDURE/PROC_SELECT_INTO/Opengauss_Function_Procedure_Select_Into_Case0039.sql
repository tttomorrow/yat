-- @testpoint: 测试利用select into语句给decimal类型的变量赋值

--前置：创建表及插入数据
drop table if exists proc_select_into_10;
create table proc_select_into_10(c_int int ,c_integer integer not null ,c_bigint bigint,c_number number default 0.2332,c_number1 number(12,2),c_number2 number(12,6),c_double binary_double,c_decimal decimal,c_decimal1 decimal(8,2),c_decimal2 decimal(8,4),c_real real,c_char char(4000),c_varchar varchar(4000),c_varchar2 varchar2(4000),c_varchar1 varchar(100),c_char1 char(100),c_numeric numeric,c_date date,c_timestamp timestamp,c_timestamp1 timestamp(6),c_bool bool) ;

insert into proc_select_into_10 values(12,58812,546223079,1234567.89,12345.6789,12.3456789,1234.56,2345.67,12345.6789,12.3456789,12.33,'dbcd','abcde','1999-01-01','ab','adc',123.45,'2005-08-08','2000-01-01 15:12:21.11','2000-08-01 15:12:21.32',true);
insert into proc_select_into_10 values(13,58813,546223078,1234567.78,12345.5678,12.2345678,1234.67,2345.78,12345.5678,12.2345678,12.44,'dbce','abcdf','abcdeg','ac','ade',123.46,'2012-08-08','2000-02-01 15:22:21.11','2012-02-01 15:12:11.32',false);
insert into proc_select_into_10 values(14,58814,546223077,1234567.67,12345.4567,12.1234567,1234.78,2345.89,12345.4567,12.1234567,12.55,'dbcf','abcdg','2010-02-28','ad','adf',123.47,'2002-08-11','2000-03-01 15:42:21.11','2008-08-12 15:13:21.32',true);
insert into proc_select_into_10 values(15,58814,546223077,1234567.67,12345.4567,12.1234567,1234.78,2345.89,12345.4567,12.1234567,12.55,'dbcf','abcdg','abcdeh','ad','adf',123.47,'2002-08-11','2000-03-01 15:42:21.11','2008-08-12 15:13:21.32',true);
insert into proc_select_into_10 values(16,58814,546223077,1234567.67,12345.4567,12.1234567,1234.78,2345.89,12345.4567,12.1234567,12.55,'dbcf','abcdg','abcdeh','ad','adf',123.47,'2002-08-11','2000-03-01 15:42:21.11','2008-08-12 15:13:21.32',true);

--创建存储过程
create or replace procedure proc_select_into_010(p_decimal2 out decimal)
as
begin
select c_decimal2 into p_decimal2 from proc_select_into_10 where c_int=12;
raise info 'p_decimal2:%',p_decimal2;
exception
when no_data_found then  raise info 'no_data_found';
end;
/
--调用存储过程
declare
v_decimal2 decimal(8,4);
begin
proc_select_into_010(v_decimal2);
end;
/
--清理环境
drop procedure proc_select_into_010;
drop table proc_select_into_10;