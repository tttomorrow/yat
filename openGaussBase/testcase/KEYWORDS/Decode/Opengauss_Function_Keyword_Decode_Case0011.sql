--  @testpoint:openGauss关键字decode(非保留)，同时作为表名和列名带引号，并进行dml操作,decode列的值最终显示为1000

drop table if exists "decode";
create table "decode"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"decode" varchar(100) default 'decode'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "decode"(c_id,"decode") values(1,'hello');
insert into "decode"(c_id,"decode") values(2,'china');
update "decode" set "decode"=1000 where "decode"='hello';
delete from "decode" where "decode"='china';
select "decode" from "decode" where "decode"!='hello' order by "decode";

drop table "decode";

