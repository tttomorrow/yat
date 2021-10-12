--  @testpoint:openGauss关键字Hold(非保留)，同时作为表名和列名带引号，并进行dml操作,Hold列的值最终显示为1000

drop table if exists "Hold";
create table "Hold"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Hold" varchar(100) default 'Hold'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "Hold"(c_id,"Hold") values(1,'hello');
insert into "Hold"(c_id,"Hold") values(2,'china');
update "Hold" set "Hold"=1000 where "Hold"='hello';
delete from "Hold" where "Hold"='china';
select "Hold" from "Hold" where "Hold"!='hello' order by "Hold";

drop table "Hold";

