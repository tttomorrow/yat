--  @testpoint:openGauss关键字duplicate(非保留),作为列名带引号并设置默认值,建表成功

drop table if exists duplicate_test;
create table duplicate_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"duplicate" text default 'gauss'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
select * from duplicate_test;
drop table duplicate_test;
