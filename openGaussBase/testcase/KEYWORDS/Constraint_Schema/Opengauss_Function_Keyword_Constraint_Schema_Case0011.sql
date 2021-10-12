--  @testpoint:openGauss关键字constraint_schema(非保留)，同时作为表名和列名带引号，并进行dml操作,constraint_schema列的值最终显示为1000

drop table if exists "constraint_schema";
create table "constraint_schema"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"constraint_schema" varchar(100) default 'constraint_schema'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "constraint_schema"(c_id,"constraint_schema") values(1,'hello');
insert into "constraint_schema"(c_id,"constraint_schema") values(2,'china');
update "constraint_schema" set "constraint_schema"=1000 where "constraint_schema"='hello';
delete from "constraint_schema" where "constraint_schema"='china';
select "constraint_schema" from "constraint_schema" where "constraint_schema"!='hello' order by "constraint_schema";

drop table "constraint_schema";

