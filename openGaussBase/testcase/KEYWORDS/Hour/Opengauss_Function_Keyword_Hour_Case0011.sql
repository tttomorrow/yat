--  @testpoint:openGauss关键字Hour(非保留)，同时作为表名和列名带引号，并进行dml操作,Hour列的值最终显示为1000

drop table if exists "Hour";
create table "Hour"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Hour" varchar(100) default 'Hour'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "Hour"(c_id,"Hour") values(1,'hello');
insert into "Hour"(c_id,"Hour") values(2,'china');
update "Hour" set "Hour"=1000 where "Hour"='hello';
delete from "Hour" where "Hour"='china';
select "Hour" from "Hour" where "Hour"!='hello' order by "Hour";

drop table "Hour";

