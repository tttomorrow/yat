--  @testpoint:openGauss关键字prefix(非保留)，同时作为表名和列名带引号，并进行dml操作,prefix列的值最终显示为1000

drop table if exists "prefix";
create table "prefix"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"prefix" varchar(100) default 'prefix'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "prefix"(c_id,"prefix") values(1,'hello');
insert into "prefix"(c_id,"prefix") values(2,'china');
update "prefix" set "prefix"=1000 where "prefix"='hello';
delete from "prefix" where "prefix"='china';
select "prefix" from "prefix" where "prefix"!='hello' order by "prefix";

drop table "prefix";

