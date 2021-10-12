--  @testpoint:openGauss关键字first(非保留)，同时作为表名和列名带引号，并进行dml操作,first列的值最终显示为1000

drop table if exists "first";
create table "first"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"first" varchar(100) default 'first'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "first"(c_id,"first") values(1,'hello');
insert into "first"(c_id,"first") values(2,'china');
update "first" set "first"=1000 where "first"='hello';
delete from "first" where "first"='china';
select "first" from "first" where "first"!='hello' order by "first";

drop table "first";

