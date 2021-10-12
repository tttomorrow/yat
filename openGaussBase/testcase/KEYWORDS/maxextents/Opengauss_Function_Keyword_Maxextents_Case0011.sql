--  @testpoint:openGauss关键字maxextents(非保留)，同时作为表名和列名带引号，并进行dml操作,maxextents列的值最终显示为1000

drop table if exists "maxextents";
create table "maxextents"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"maxextents" varchar(100) default 'maxextents'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "maxextents"(c_id,"maxextents") values(1,'hello');
insert into "maxextents"(c_id,"maxextents") values(2,'china');
update "maxextents" set "maxextents"=1000 where "maxextents"='hello';
delete from "maxextents" where "maxextents"='china';
select "maxextents" from "maxextents" where "maxextents"!='hello' order by "maxextents";

drop table "maxextents";
