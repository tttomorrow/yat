--  @testpoint:openGauss关键字rebuild(非保留)，同时作为表名和列名带引号，并进行dml操作,rebuild列的值最终显示为1000

drop table if exists "rebuild";
create table "rebuild"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"rebuild" varchar(100) default 'rebuild'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "rebuild"(c_id,"rebuild") values(1,'hello');
insert into "rebuild"(c_id,"rebuild") values(2,'china');
update "rebuild" set "rebuild"=1000 where "rebuild"='hello';
delete from "rebuild" where "rebuild"='china';
select "rebuild" from "rebuild" where "rebuild"!='hello' order by "rebuild";

drop table "rebuild";

