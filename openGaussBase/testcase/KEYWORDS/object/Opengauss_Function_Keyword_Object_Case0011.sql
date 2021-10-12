--  @testpoint:openGauss关键字object(非保留)，同时作为表名和列名带引号，并进行dml操作,object列的值最终显示为1000

drop table if exists "object";
create table "object"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"object" varchar(100) default 'object'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "object"(c_id,"object") values(1,'hello');
insert into "object"(c_id,"object") values(2,'china');
update "object" set "object"=1000 where "object"='hello';
delete from "object" where "object"='china';
select "object" from "object" where "object"!='hello' order by "object";

drop table "object";
