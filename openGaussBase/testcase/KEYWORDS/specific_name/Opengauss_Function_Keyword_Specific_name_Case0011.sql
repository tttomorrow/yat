--  @testpoint:openGauss关键字specific_name(非保留)，同时作为表名和列名带引号，并进行dml操作,specific_name列的值最终显示为1000

drop table if exists "specific_name" CASCADE;
create table "specific_name"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"specific_name" varchar(100) default 'specific_name'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "specific_name"(c_id,"specific_name") values(1,'hello');
insert into "specific_name"(c_id,"specific_name") values(2,'china');
update "specific_name" set "specific_name"=1000 where "specific_name"='hello';
delete from "specific_name" where "specific_name"='china';
select "specific_name" from "specific_name" where "specific_name"!='hello' order by "specific_name";

drop table "specific_name";

