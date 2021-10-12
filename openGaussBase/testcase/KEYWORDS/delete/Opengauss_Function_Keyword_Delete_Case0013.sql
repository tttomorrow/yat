--  @testpoint:openGauss关键字delete(非保留)，同时作为表名和列名带引号，与union结合查询合并两个SELECT 语句查询

drop table if exists "delete";
create table "delete"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"delete" varchar(100) default 'delete'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

insert into "delete"(c_id,"delete") values(1,'hello');
insert into "delete"(c_id,"delete") values(2,'china');
insert into "delete"(c_id,"delete") values(3,'gauss');
---两个select语句合并查询，查询结果显示hello、china、gauss，对括号中的select子句取limit 2
select "delete" from "delete" where "delete"='hello'
union all (select "delete" from "delete" where "delete"!='hello' order by "delete" limit 2);

drop table "delete";
