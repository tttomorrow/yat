--  @testpoint:openGauss关键字spill(非保留)，同时作为表名和列名带引号，并进行dml操作,spill列的值最终显示为1000

drop table if exists "spill" CASCADE;
create table "spill"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"spill" varchar(100) default 'spill'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "spill"(c_id,"spill") values(1,'hello');
insert into "spill"(c_id,"spill") values(2,'china');
update "spill" set "spill"=1000 where "spill"='hello';
delete from "spill" where "spill"='china';
select "spill" from "spill" where "spill"!='hello' order by "spill";

drop table "spill";

