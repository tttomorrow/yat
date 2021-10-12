--  @testpoint:openGauss关键字trigger_name(非保留)，同时作为表名和列名带引号，并进行dml操作,trigger_name列的值最终显示为1000

drop table if exists "trigger_name" CASCADE;
create table "trigger_name"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"trigger_name" varchar(100) default 'trigger_name'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "trigger_name"(c_id,"trigger_name") values(1,'hello');
insert into "trigger_name"(c_id,"trigger_name") values(2,'china');
update "trigger_name" set "trigger_name"=1000 where "trigger_name"='hello';
delete from "trigger_name" where "trigger_name"='china';
select "trigger_name" from "trigger_name" where "trigger_name"!='hello' order by "trigger_name";

drop table "trigger_name";

