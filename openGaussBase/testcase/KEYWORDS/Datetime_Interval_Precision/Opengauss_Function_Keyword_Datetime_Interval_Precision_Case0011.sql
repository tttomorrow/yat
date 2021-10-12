--  @testpoint:openGauss关键字datetime_interval_precision(非保留)，同时作为表名和列名带引号，并进行dml操作,datetime_interval_precision列的值最终显示为1000

drop table if exists "datetime_interval_precision";
create table "datetime_interval_precision"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"datetime_interval_precision" varchar(100) default 'datetime_interval_precision'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "datetime_interval_precision"(c_id,"datetime_interval_precision") values(1,'hello');
insert into "datetime_interval_precision"(c_id,"datetime_interval_precision") values(2,'china');
update "datetime_interval_precision" set "datetime_interval_precision"=1000 where "datetime_interval_precision"='hello';
delete from "datetime_interval_precision" where "datetime_interval_precision"='china';
select "datetime_interval_precision" from "datetime_interval_precision" where "datetime_interval_precision"!='hello' order by "datetime_interval_precision";

drop table "datetime_interval_precision";

