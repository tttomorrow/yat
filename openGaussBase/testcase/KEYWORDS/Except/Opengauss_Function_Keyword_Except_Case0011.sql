--  @testpoint:openGauss保留关键字except同时作为表名和列名带引号，并进行dml操作,except列的值最终显示为1000
drop table if exists "except";
create table "except"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_exceptuble real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"except" varchar(100) default 'except'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "except"(c_id,"except") values(1,'hello');
insert into "except"(c_id,"except") values(2,'china');
update "except" set "except"=1000 where "except"='hello';
delete from "except" where "except"='china';
select "except" from "except" where "except"!='hello' order by "except";

drop table "except";