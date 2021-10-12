-- @testpoint: openGauss关键字Committed(非保留),作为列名不带双引号，Committed大小写混合，建表成功

drop table if exists Committed_test;
create table Committed_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	Committed text
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
--openGauss关键字committed(非保留),作为列名不带双引号，committed大小匹配，建表成功
drop table if exists committed_test;
create table committed_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	committed text
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
drop table if exists Committed_test;
drop table if exists committed_test;