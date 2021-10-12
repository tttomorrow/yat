--  @testpoint:openGauss关键字terminate(非保留)，同时作为表名和列名带引号，并进行dml操作,terminate列的值最终显示为1000

drop table if exists "terminate" CASCADE;
create table "terminate"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"terminate" varchar(100) default 'terminate'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "terminate"(c_id,"terminate") values(1,'hello');
insert into "terminate"(c_id,"terminate") values(2,'china');
update "terminate" set "terminate"=1000 where "terminate"='hello';
delete from "terminate" where "terminate"='china';
select "terminate" from "terminate" where "terminate"!='hello' order by "terminate";

drop table "terminate";

