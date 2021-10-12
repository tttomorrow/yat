--  @testpoint:openGauss关键字mod(非保留)，同时作为表名和列名带引号，并进行dml操作,mod列的值最终显示为1000

drop table if exists "mod";
create table "mod"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"mod" varchar(100) default 'mod'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "mod"(c_id,"mod") values(1,'hello');
insert into "mod"(c_id,"mod") values(2,'china');
update "mod" set "mod"=1000 where "mod"='hello';
delete from "mod" where "mod"='china';
select "mod" from "mod" where "mod"!='hello' order by "mod";

drop table "mod";

