--  @testpoint:openGauss关键字deterministic(非保留)，同时作为表名和列名带引号，并进行dml操作,deterministic列的值最终显示为1000

drop table if exists "deterministic";
create table "deterministic"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"deterministic" varchar(100) default 'deterministic'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "deterministic"(c_id,"deterministic") values(1,'hello');
insert into "deterministic"(c_id,"deterministic") values(2,'china');
update "deterministic" set "deterministic"=1000 where "deterministic"='hello';
delete from "deterministic" where "deterministic"='china';
select "deterministic" from "deterministic" where "deterministic"!='hello' order by "deterministic";

drop table "deterministic";

