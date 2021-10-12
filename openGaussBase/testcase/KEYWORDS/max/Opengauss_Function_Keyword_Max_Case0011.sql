--  @testpoint:openGauss关键字max(非保留)，同时作为表名和列名带引号，并进行dml操作,max列的值最终显示为1000

drop table if exists "max";
create table "max"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"max" varchar(100) default 'max'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "max"(c_id,"max") values(1,'hello');
insert into "max"(c_id,"max") values(2,'china');
update "max" set "max"=1000 where "max"='hello';
delete from "max" where "max"='china';
select "max" from "max" where "max"!='hello' order by "max";

drop table "max";
