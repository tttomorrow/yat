--  @testpoint:openGauss关键字nothing(非保留)，同时作为表名和列名带引号，并进行dml操作,nothing列的值最终显示为1000

drop table if exists "nothing";
create table "nothing"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"nothing" varchar(100) default 'nothing'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "nothing"(c_id,"nothing") values(1,'hello');
insert into "nothing"(c_id,"nothing") values(2,'china');
update "nothing" set "nothing"=1000 where "nothing"='hello';
delete from "nothing" where "nothing"='china';
select "nothing" from "nothing" where "nothing"!='hello' order by "nothing";

drop table "nothing";

