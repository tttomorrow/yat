--  @testpoint:openGauss关键字replace(非保留)，同时作为表名和列名带引号，并进行dml操作,replace列的值最终显示为1000

drop table if exists "replace";
create table "replace"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"replace" varchar(100) default 'replace'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "replace"(c_id,"replace") values(1,'hello');
insert into "replace"(c_id,"replace") values(2,'china');
update "replace" set "replace"=1000 where "replace"='hello';
delete from "replace" where "replace"='china';
select "replace" from "replace" where "replace"!='hello' order by "replace";

drop table "replace";

