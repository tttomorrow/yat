--  @testpoint:openGauss关键字percent(非保留)，同时作为表名和列名带引号，并进行dml操作,percent列的值最终显示为1000

drop table if exists "percent";
create table "percent"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"percent" varchar(100) default 'percent'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "percent"(c_id,"percent") values(1,'hello');
insert into "percent"(c_id,"percent") values(2,'china');
update "percent" set "percent"=1000 where "percent"='hello';
delete from "percent" where "percent"='china';
select "percent" from "percent" where "percent"!='hello' order by "percent";

drop table "percent";

