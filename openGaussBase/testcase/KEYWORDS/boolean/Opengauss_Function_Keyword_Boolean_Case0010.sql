--  @testpoint:openGauss关键字boolean(非保留),同时作为表名和列名带引号，建表成功
--创建表
drop table if exists "boolean";
create table "boolean"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"boolean" varchar(100) default 'boolean'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--查询表内容
select * from "boolean";

--清理环境
drop table "boolean";
