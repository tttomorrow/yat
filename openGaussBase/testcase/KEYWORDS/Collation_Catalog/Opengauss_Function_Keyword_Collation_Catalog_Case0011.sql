--  @testpoint:openGauss关键字collation_catalog(非保留)，同时作为表名和列名带引号，并进行dml操作,collation_catalog列的值最终显示为1000

drop table if exists "collation_catalog";
create table "collation_catalog"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"collation_catalog" varchar(100) default 'collation_catalog'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "collation_catalog"(c_id,"collation_catalog") values(1,'hello');
insert into "collation_catalog"(c_id,"collation_catalog") values(2,'china');
update "collation_catalog" set "collation_catalog"=1000 where "collation_catalog"='hello';
delete from "collation_catalog" where "collation_catalog"='china';
select "collation_catalog" from "collation_catalog" where "collation_catalog"!='hello' order by "collation_catalog";

drop table "collation_catalog";

