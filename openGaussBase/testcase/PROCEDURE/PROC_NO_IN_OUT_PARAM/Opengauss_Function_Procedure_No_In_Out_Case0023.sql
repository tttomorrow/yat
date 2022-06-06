-- @testpoint: 测试无出入参存储过程（测试变量为bool型无入出参存储过程）

drop table if exists proc_no_in_out_param_001;
create table proc_no_in_out_param_001(
c_int int ,
c_integer integer not null ,
c_bigint bigint,
c_number number default 0.2332,
c_number1 number(12,2),
c_number2 number(12,6),
c_binary binary_double,
c_decimal decimal,
c_decimal1 decimal(8,2),
c_decimal2 decimal(8,4),
c_real real,c_char char(4000),
c_varchar varchar(4000),
c_varchar2 varchar2(4000),
c_varchar1 varchar(100),
c_char1 char(100),
c_numeric numeric,
c_date date,
c_timestamp timestamp,
c_timestamp1 timestamp(6),
c_bool bool
) ;

drop index if exists indx_t1 ;
create unique index  indx_t1 on proc_no_in_out_param_001 (c_int);
drop index  if exists indx_t2;
create index indx_t2 on proc_no_in_out_param_001 (c_int,c_timestamp);

insert into proc_no_in_out_param_001 values(12,58812,546223079,1234567.89,12345.6789,12.3456789,1234.56,2345.67,12345.6789,12.3456789,12.33,'dbcd','abcde','1999-01-01','ab','adc',123.45,'2005-08-08','2000-01-01 15:12:21.11','2000-08-01 15:12:21.32',true);
insert into proc_no_in_out_param_001 values(13,58813,546223078,1234567.78,12345.5678,12.2345678,1234.67,2345.78,12345.5678,12.2345678,12.44,'dbce','abcdf','abcdeg','ac','ade',123.46,'2012-08-08','2000-02-01 15:22:21.11','2012-02-01 15:12:11.32',false);
insert into proc_no_in_out_param_001 values(14,58814,546223077,1234567.67,12345.4567,12.1234567,1234.78,2345.89,12345.4567,12.1234567,12.55,'dbcf','abcdg','2010-02-28','ad','adf',123.47,'2002-08-11','2000-03-01 15:42:21.11','2008-08-12 15:13:21.32',true);
insert into proc_no_in_out_param_001 values(15,58814,546223077,1234567.67,12345.4567,12.1234567,1234.78,2345.89,12345.4567,12.1234567,12.55,'dbcf','abcdg','abcdeh','ad','adf',123.47,'2002-08-11','2000-03-01 15:42:21.11','2008-08-12 15:13:21.32',true);
insert into proc_no_in_out_param_001 values(16,58814,546223077,1234567.67,12345.4567,12.1234567,1234.78,2345.89,12345.4567,12.1234567,12.55,'dbcf','abcdg','abcdeh','ad','adf',123.47,'2002-08-11','2000-03-01 15:42:21.11','2008-08-12 15:13:21.32',true);


create or replace procedure proc_no_in_out_param_022 as
v_bool bool;
begin
select c_bool into v_bool from proc_no_in_out_param_001 where c_int=12;
raise info ':%',v_bool;
exception
when no_data_found then raise info 'no_data_found';
end;
/

call proc_no_in_out_param_022();
drop procedure proc_no_in_out_param_022;
drop table if exists proc_no_in_out_param_001;