--  @testpoint:openGauss关键字merge(非保留)，同时作为表名和列名带引号，并进行dml操作,merge列的值最终显示为1000

drop table if exists "merge";
create table "merge"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"merge" varchar(100) default 'merge'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "merge"(c_id,"merge") values(1,'hello');
insert into "merge"(c_id,"merge") values(2,'china');
update "merge" set "merge"=1000 where "merge"='hello';
delete from "merge" where "merge"='china';
select "merge" from "merge" where "merge"!='hello' order by "merge";

drop table "merge";

