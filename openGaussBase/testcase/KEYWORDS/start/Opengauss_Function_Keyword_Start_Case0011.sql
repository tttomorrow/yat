--  @testpoint:openGauss关键字start(非保留)，同时作为表名和列名带引号，并进行dml操作,start列的值最终显示为1000

drop table if exists "start" CASCADE;
create table "start"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"start" varchar(100) default 'start'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "start"(c_id,"start") values(1,'hello');
insert into "start"(c_id,"start") values(2,'china');
update "start" set "start"=1000 where "start"='hello';
delete from "start" where "start"='china';
select "start" from "start" where "start"!='hello' order by "start";

drop table "start";

