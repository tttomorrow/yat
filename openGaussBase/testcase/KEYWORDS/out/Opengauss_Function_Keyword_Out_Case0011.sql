--  @testpoint:openGauss关键字out(非保留)，同时作为表名和列名带引号，并进行dml操作,out列的值最终显示为1000

drop table if exists "out";
create table "out"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"out" varchar(100) default 'out'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "out"(c_id,"out") values(1,'hello');
insert into "out"(c_id,"out") values(2,'china');
update "out" set "out"=1000 where "out"='hello';
delete from "out" where "out"='china';
select "out" from "out" where "out"!='hello' order by "out";

drop table "out";

