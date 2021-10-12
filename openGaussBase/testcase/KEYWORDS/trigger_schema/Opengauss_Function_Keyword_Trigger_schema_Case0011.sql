--  @testpoint:openGauss关键字trigger_schema(非保留)，同时作为表名和列名带引号，并进行dml操作,trigger_schema列的值最终显示为1000

drop table if exists "trigger_schema" CASCADE;
create table "trigger_schema"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"trigger_schema" varchar(100) default 'trigger_schema'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "trigger_schema"(c_id,"trigger_schema") values(1,'hello');
insert into "trigger_schema"(c_id,"trigger_schema") values(2,'china');
update "trigger_schema" set "trigger_schema"=1000 where "trigger_schema"='hello';
delete from "trigger_schema" where "trigger_schema"='china';
select "trigger_schema" from "trigger_schema" where "trigger_schema"!='hello' order by "trigger_schema";

drop table "trigger_schema";

