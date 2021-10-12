--  @testpoint:openGauss关键字sqlcode(非保留)，同时作为表名和列名带引号，并进行dml操作,sqlcode列的值最终显示为1000

drop table if exists "sqlcode" CASCADE;
create table "sqlcode"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"sqlcode" varchar(100) default 'sqlcode'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "sqlcode"(c_id,"sqlcode") values(1,'hello');
insert into "sqlcode"(c_id,"sqlcode") values(2,'china');
update "sqlcode" set "sqlcode"=1000 where "sqlcode"='hello';
delete from "sqlcode" where "sqlcode"='china';
select "sqlcode" from "sqlcode" where "sqlcode"!='hello' order by "sqlcode";

drop table "sqlcode";

