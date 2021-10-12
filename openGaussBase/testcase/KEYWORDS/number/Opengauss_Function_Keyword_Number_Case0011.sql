--  @testpoint:openGauss关键字number(非保留)，同时作为表名和列名带引号，并进行dml操作,number列的值最终显示为1000

drop table if exists "number";
create table "number"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"number" varchar(100) default 'number'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "number"(c_id,"number") values(1,'hello');
insert into "number"(c_id,"number") values(2,'china');
update "number" set "number"=1000 where "number"='hello';
delete from "number" where "number"='china';
select "number" from "number" where "number"!='hello' order by "number";

drop table "number";

