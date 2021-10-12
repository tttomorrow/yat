--  @testpoint:openGauss关键字cursor_name(非保留),同时作为表名和列名带引号，建表成功

drop table if exists "cursor_name";
create table "cursor_name"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"cursor_name" varchar(100) default 'cursor_name'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
select * from  "cursor_name";
drop table "cursor_name";
