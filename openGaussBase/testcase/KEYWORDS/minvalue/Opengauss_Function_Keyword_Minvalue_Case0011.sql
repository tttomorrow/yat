--  @testpoint:openGauss关键字minvalue(非保留)，同时作为表名和列名带引号，并进行dml操作,minvalue列的值最终显示为1000

drop table if exists "minvalue";
create table "minvalue"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"minvalue" varchar(100) default 'minvalue'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "minvalue"(c_id,"minvalue") values(1,'hello');
insert into "minvalue"(c_id,"minvalue") values(2,'china');
update "minvalue" set "minvalue"=1000 where "minvalue"='hello';
delete from "minvalue" where "minvalue"='china';
select "minvalue" from "minvalue" where "minvalue"!='hello' order by "minvalue";

drop table "minvalue";

