--  @testpoint:openGauss关键字float(非保留)，作为列名带引号并且排序时使用该列,建表成功，float列按字母大小排序

drop table if exists float_test;
create table float_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"float" varchar(100) default 'float'
) 
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

insert into float_test(c_id,"float") values(1,'hello');
select * from float_test order by "float";
drop table float_test;

