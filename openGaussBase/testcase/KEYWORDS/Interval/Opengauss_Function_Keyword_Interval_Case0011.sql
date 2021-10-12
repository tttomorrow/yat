--  @testpoint:openGauss关键字Interval(非保留)，同时作为表名和列名带引号，并进行dml操作,Interval列的值最终显示为1000

drop table if exists "Interval";
create table "Interval"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Interval" varchar(100) default 'Interval'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "Interval"(c_id,"Interval") values(1,'hello');
insert into "Interval"(c_id,"Interval") values(2,'china');
update "Interval" set "Interval"=1000 where "Interval"='hello';
delete from "Interval" where "Interval"='china';
select "Interval" from "Interval" where "Interval"!='hello' order by "Interval";

drop table "Interval";

