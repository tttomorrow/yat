--  @testpoint:openGauss关键字constraint_schema(非保留)同时作为表名和列名带引号,并使用该列结合limit排序,constraint_schema列的值按字母大小排序且只显示前2条数据

drop table if exists "constraint_schema";
create table "constraint_schema"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"constraint_schema" varchar(100) default 'constraint_schema'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);
delete from "constraint_schema";
insert into "constraint_schema"(c_id,"constraint_schema") values(1,'hello');
insert into "constraint_schema"(c_id,"constraint_schema") values(2,'china');
insert into "constraint_schema"(c_id,"constraint_schema") values(3,'gauss');
select "constraint_schema" from "constraint_schema" where "constraint_schema"!='hello' order by "constraint_schema" limit 2 ;

drop table "constraint_schema";

