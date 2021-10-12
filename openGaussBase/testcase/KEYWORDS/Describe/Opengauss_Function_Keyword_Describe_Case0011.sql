--  @testpoint:openGauss关键字describe(非保留)，同时作为表名和列名带引号，并进行dml操作,describe列的值最终显示为1000

drop table if exists "describe";
create table "describe"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"describe" varchar(100) default 'describe'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "describe"(c_id,"describe") values(1,'hello');
insert into "describe"(c_id,"describe") values(2,'china');
update "describe" set "describe"=1000 where "describe"='hello';
delete from "describe" where "describe"='china';
select "describe" from "describe" where "describe"!='hello' order by "describe";

drop table "describe";
