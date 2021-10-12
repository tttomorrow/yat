--  @testpoint:openGauss关键字Command_Function_Code(非保留),作为列名带双引号，Command_Function_Code大小写混合，建表成功

drop table if exists Command_Function_Code_test;
create table Command_Function_Code_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Command_Function_Code" char(50)
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

select * from Command_Function_Code_test;
drop table Command_Function_Code_test;
--openGauss关键字command_function_code(非保留),作为列名带双引号，command_function_code大小写匹配，建表成功

drop table if exists command_function_code_test;
create table command_function_code_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"command_function_code" char(50)
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

select * from command_function_code_test;
drop table command_function_code_test;