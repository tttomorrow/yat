--  @testpoint:openGauss关键字dispatch(非保留),作为列名带引号并设置默认值,建表成功

drop table if exists dispatch_test;
create table dispatch_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"dispatch" text default 'gauss'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
select * from dispatch_test;
drop table dispatch_test;
