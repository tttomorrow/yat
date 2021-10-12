--  @testpoint:openGauss关键字decimal(非保留)，同时作为表名和列名带引号，并进行dml操作,decimal列的值最终显示为1000

drop table if exists "decimal";
create table "decimal"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"decimal" varchar(100) default 'decimal'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "decimal"(c_id,"decimal") values(1,'hello');
insert into "decimal"(c_id,"decimal") values(2,'china');
update "decimal" set "decimal"=1000 where "decimal"='hello';
delete from "decimal" where "decimal"='china';
select "decimal" from "decimal" where "decimal"!='hello' order by "decimal";

drop table "decimal";
