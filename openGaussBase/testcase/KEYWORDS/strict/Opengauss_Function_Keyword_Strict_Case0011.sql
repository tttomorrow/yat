--  @testpoint:openGauss关键字strict(非保留)，同时作为表名和列名带引号，并进行dml操作,strict列的值最终显示为1000

drop table if exists "strict" CASCADE;
create table "strict"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"strict" varchar(100) default 'strict'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "strict"(c_id,"strict") values(1,'hello');
insert into "strict"(c_id,"strict") values(2,'china');
update "strict" set "strict"=1000 where "strict"='hello';
delete from "strict" where "strict"='china';
select "strict" from "strict" where "strict"!='hello' order by "strict";

drop table "strict";

