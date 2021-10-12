--  @testpoint:openGauss关键字second(非保留)，同时作为表名和列名带引号，并进行dml操作,second列的值最终显示为1000

drop table if exists "second" CASCADE;
create table "second"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"second" varchar(100) default 'second'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "second"(c_id,"second") values(1,'hello');
insert into "second"(c_id,"second") values(2,'china');
update "second" set "second"=1000 where "second"='hello';
delete from "second" where "second"='china';
select "second" from "second" where "second"!='hello' order by "second";

drop table "second";

