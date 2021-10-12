-- @testpoint: openGauss关键字concurrently(非保留),作为列名带双引号，使用时不带，部分测试点合理报错

drop table if exists concurrently_test;
create table concurrently_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"concurrently" char(50)	
) 
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
insert into concurrently_test(c_id,concurrently) values(2,'china');
drop table if exists concurrently_test;