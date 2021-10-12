--  @testpoint:openGauss关键字collation_name(非保留)，同时作为表名和列名带引号，并进行dml操作,collation_name列的值最终显示为1000

drop table if exists "collation_name";
create table "collation_name"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"collation_name" varchar(100) default 'collation_name'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "collation_name"(c_id,"collation_name") values(1,'hello');
insert into "collation_name"(c_id,"collation_name") values(2,'china');
update "collation_name" set "collation_name"=1000 where "collation_name"='hello';
delete from "collation_name" where "collation_name"='china';
select "collation_name" from "collation_name" where "collation_name"!='hello' order by "collation_name";

drop table "collation_name";

