--  @testpoint:openGauss保留关键字current_catalog同时作为表名和列名带引号，建表成功
drop table if exists "current_catalog";
create table "current_catalog"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"current_catalog" varchar(100) default 'current_catalog'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--查看表数据
select "current_catalog" from "current_catalog";

--清理环境
drop table "current_catalog";