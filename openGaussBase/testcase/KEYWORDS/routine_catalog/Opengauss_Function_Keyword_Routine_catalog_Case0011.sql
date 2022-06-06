--  @testpoint:openGauss关键字routine_catalog(非保留)，同时作为表名和列名带引号，并进行dml操作,routine_catalog列的值最终显示为1000

drop table if exists "routine_catalog" CASCADE;
create table "routine_catalog"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"routine_catalog" varchar(100) default 'routine_catalog'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "routine_catalog"(c_id,"routine_catalog") values(1,'hello');
insert into "routine_catalog"(c_id,"routine_catalog") values(2,'china');
update "routine_catalog" set "routine_catalog"=1000 where "routine_catalog"='hello';
delete from "routine_catalog" where "routine_catalog"='china';
select "routine_catalog" from "routine_catalog" where "routine_catalog"!='hello' order by "routine_catalog";

drop table "routine_catalog";

