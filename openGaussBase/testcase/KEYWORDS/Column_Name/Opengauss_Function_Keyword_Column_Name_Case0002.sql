--  @testpoint:openGauss关键字Column_Name(非保留),作为列名带双引号，Column_Name大小写混合，建表成功

drop table if exists Column_Name_test;
create table Column_Name_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Column_Name" char(50)
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

select * from Column_Name_test;
drop table Column_Name_test;
--openGauss关键字column_name(非保留),作为列名带双引号，column_name大小写匹配，建表成功

drop table if exists column_name_test;
create table column_name_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"column_name" char(50)
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

select * from column_name_test;
drop table column_name_test;