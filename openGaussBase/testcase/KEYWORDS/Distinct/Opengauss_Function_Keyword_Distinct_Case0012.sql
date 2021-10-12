--  @testpoint:openGauss保留关键字distinct同时作为表名和列名带引号,并使用该列结合limit排序,distinct列的值按字母大小排序且只显示前2条数据
drop table if exists "distinct";
create table "distinct"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"distinct" varchar(100) default 'distinct'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
delete from "distinct";
insert into "distinct"(c_id,"distinct") values(1,'hello');
insert into "distinct"(c_id,"distinct") values(2,'china');
insert into "distinct"(c_id,"distinct") values(3,'gauss');
select "distinct" from "distinct" where "distinct"!='hello' order by "distinct" limit 2 ;

drop table "distinct";