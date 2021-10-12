--  @testpoint:openGauss关键字types(非保留)，同时作为表名和列名带引号，并进行dml操作,types列的值最终显示为1000

drop table if exists "types" CASCADE;
create table "types"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"types" varchar(100) default 'types'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "types"(c_id,"types") values(1,'hello');
insert into "types"(c_id,"types") values(2,'china');
update "types" set "types"=1000 where "types"='hello';
delete from "types" where "types"='china';
select "types" from "types" where "types"!='hello' order by "types";

drop table "types";

