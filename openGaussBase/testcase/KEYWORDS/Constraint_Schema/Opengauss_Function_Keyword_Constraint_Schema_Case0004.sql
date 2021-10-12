--  @testpoint:openGauss关键字constraint_schema(非保留),作为列名不带引号，使用时带双引号或反引号，大小写匹配,失败

drop table if exists constraint_schema_test;
create table constraint_schema_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	constraint_schema char(50)
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
insert into constraint_schema_test(c_id,"constraint_schema") values(2,'china');
insert into constraint_schema_test(c_id,`constraint_schema`) values(2,'china');
