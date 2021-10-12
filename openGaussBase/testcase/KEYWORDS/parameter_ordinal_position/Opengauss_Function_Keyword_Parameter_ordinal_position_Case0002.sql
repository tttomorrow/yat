--  @testpoint:openGauss关键字Parameter_ordinal_position(非保留),作为列名带双引号，Parameter_ordinal_position大小写混合，建表成功

drop table if exists Explain_test;
create table Explain_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Parameter_ordinal_position" char(50)
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

select * from Explain_test;
drop table Explain_test;

--openGauss关键字parameter_ordinal_position(非保留),作为列名带双引号，parameter_ordinal_position大小写匹配，建表成功
drop table if exists Explain_test;
create table Explain_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"parameter_ordinal_position" char(50)
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

select * from Explain_test;
drop table Explain_test;