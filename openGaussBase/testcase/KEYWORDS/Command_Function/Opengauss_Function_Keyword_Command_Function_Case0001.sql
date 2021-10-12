-- @testpoint: openGauss关键字Command_Function(非保留),作为列名不带双引号，Command_Function大小写混合，建表成功

drop table if exists Command_Function_test;
create table Command_Function_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	Command_Function text
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
--openGauss关键字command_function(非保留),作为列名不带双引号，command_function大小匹配，建表成功
drop table if exists Collation_Catalog_test;
create table Collation_Catalog_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	command_function text
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
drop table if exists Command_Function_test;
drop table if exists Collation_Catalog_test;