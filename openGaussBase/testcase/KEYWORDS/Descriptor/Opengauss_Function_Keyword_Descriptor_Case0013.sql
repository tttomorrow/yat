--  @testpoint:openGauss关键字descriptor(非保留)，同时作为表名和列名带引号，与union结合查询合并两个SELECT 语句查询

drop table if exists "descriptor";
create table "descriptor"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"descriptor" varchar(100) default 'descriptor'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

insert into "descriptor"(c_id,"descriptor") values(1,'hello');
insert into "descriptor"(c_id,"descriptor") values(2,'china');
insert into "descriptor"(c_id,"descriptor") values(3,'gauss');
---两个select语句合并查询，查询结果显示hello、china、gauss，对括号中的select子句取limit 2
select "descriptor" from "descriptor" where "descriptor"='hello'
union all (select "descriptor" from "descriptor" where "descriptor"!='hello' order by "descriptor" limit 2);

drop table "descriptor";