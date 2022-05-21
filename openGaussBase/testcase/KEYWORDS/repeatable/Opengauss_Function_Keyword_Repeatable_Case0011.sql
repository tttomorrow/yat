--  @testpoint:openGauss关键字repeatable(非保留)，同时作为表名和列名带引号，并进行dml操作,repeatable列的值最终显示为1000

drop table if exists "repeatable";
create table "repeatable"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"repeatable" varchar(100) default 'repeatable'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "repeatable"(c_id,"repeatable") values(1,'hello');
insert into "repeatable"(c_id,"repeatable") values(2,'china');
update "repeatable" set "repeatable"=1000 where "repeatable"='hello';
delete from "repeatable" where "repeatable"='china';
select "repeatable" from "repeatable" where "repeatable"!='hello' order by "repeatable";

drop table "repeatable";

