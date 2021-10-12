--  @testpoint:openGauss关键字definer(非保留)同时作为表名和列名带引号,并使用该列结合limit排序,definer列的值按字母大小排序且只显示前2条数据

drop table if exists "definer";
create table "definer"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"definer" varchar(100) default 'definer'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
delete from "definer";
insert into "definer"(c_id,"definer") values(1,'hello');
insert into "definer"(c_id,"definer") values(2,'china');
insert into "definer"(c_id,"definer") values(3,'gauss');
select "definer" from "definer" where "definer"!='hello' order by "definer" limit 2 ;

drop table "definer";

