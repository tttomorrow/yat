--  @testpoint:openGauss关键字match(非保留)，同时作为表名和列名带引号，并进行dml操作,match列的值最终显示为1000

drop table if exists "match";
create table "match"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"match" varchar(100) default 'match'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "match"(c_id,"match") values(1,'hello');
insert into "match"(c_id,"match") values(2,'china');
update "match" set "match"=1000 where "match"='hello';
delete from "match" where "match"='china';
select "match" from "match" where "match"!='hello' order by "match";

drop table "match";

