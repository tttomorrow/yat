--  @testpoint:openGauss关键字timezone_hour(非保留)，同时作为表名和列名带引号，并进行dml操作,timezone_hour列的值最终显示为1000

drop table if exists "timezone_hour" CASCADE;
create table "timezone_hour"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"timezone_hour" varchar(100) default 'timezone_hour'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "timezone_hour"(c_id,"timezone_hour") values(1,'hello');
insert into "timezone_hour"(c_id,"timezone_hour") values(2,'china');
update "timezone_hour" set "timezone_hour"=1000 where "timezone_hour"='hello';
delete from "timezone_hour" where "timezone_hour"='china';
select "timezone_hour" from "timezone_hour" where "timezone_hour"!='hello' order by "timezone_hour";

drop table "timezone_hour";

