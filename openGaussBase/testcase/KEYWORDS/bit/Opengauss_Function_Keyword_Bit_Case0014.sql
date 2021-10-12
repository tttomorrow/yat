--  @testpoint:openGauss关键字bit(非保留)，作为列名带单引号,合理报错
--创建表
drop table if exists bit_test;
create table bit_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	'bit' varchar(100)
);
--未创建成功无需清理环境