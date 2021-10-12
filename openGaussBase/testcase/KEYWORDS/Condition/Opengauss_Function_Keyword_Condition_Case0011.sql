--  @testpoint:openGauss关键字condition(非保留)，同时作为表名和列名带引号，并进行dml操作,condition列的值最终显示为1000

drop table if exists "condition";
create table "condition"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"condition" varchar(100) default 'condition'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "condition"(c_id,"condition") values(1,'hello');
insert into "condition"(c_id,"condition") values(2,'china');
update "condition" set "condition"=1000 where "condition"='hello';
delete from "condition" where "condition"='china';
select "condition" from "condition" where "condition"!='hello' order by "condition";

drop table "condition";
