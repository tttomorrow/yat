--  @testpoint:openGauss关键字descriptor(非保留)，同时作为表名和列名带引号，并进行dml操作,descriptor列的值最终显示为1000

drop table if exists "descriptor";
create table "descriptor"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"descriptor" varchar(100) default 'descriptor'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "descriptor"(c_id,"descriptor") values(1,'hello');
insert into "descriptor"(c_id,"descriptor") values(2,'china');
update "descriptor" set "descriptor"=1000 where "descriptor"='hello';
delete from "descriptor" where "descriptor"='china';
select "descriptor" from "descriptor" where "descriptor"!='hello' order by "descriptor";

drop table "descriptor";

