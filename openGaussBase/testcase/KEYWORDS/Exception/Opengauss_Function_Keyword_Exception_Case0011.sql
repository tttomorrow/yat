-- @testpoint: openGauss关键字Exception(非保留)，同时作为表名和列名带引号，并进行dml操作,Exception列的值最终显示为1000

drop table if exists "Exception";
create table "Exception"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Exception" varchar(100) default 'Exception'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "Exception"(c_id,"Exception") values(1,'hello');
insert into "Exception"(c_id,"Exception") values(2,'china');
update "Exception" set "Exception"=1000 where "Exception"='hello';
delete from "Exception" where "Exception"='china';
select "Exception" from "Exception" where "Exception"!='hello' order by "Exception";

drop table "Exception";

