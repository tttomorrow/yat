-- @testpoint: openGauss关键字Contains(非保留),作为列名不带双引号，Contains大小写混合，建表成功

drop table if exists Contains_test;
create table Contains_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	Contains text
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
--openGauss关键字contains(非保留),作为列名不带双引号，contains大小匹配，建表成功
drop table if exists Collation_Catalog_test;
create table Collation_Catalog_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	contains text
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
drop table if exists Contains_test;
drop table if exists Collation_Catalog_test;