--  @testpoint:openGauss关键字character_set_name(非保留)，同时作为表名和列名带引号，与union结合查询合并两个SELECT 语句查询
--创建表
drop table if exists "character_set_name";
create table "character_set_name"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"character_set_name" varchar(100) default 'character_set_name'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--向表中插入数据
insert into "character_set_name"(c_id,"character_set_name") values(1,'hello');
insert into "character_set_name"(c_id,"character_set_name") values(2,'china');
insert into "character_set_name"(c_id,"character_set_name") values(3,'gauss');

---两个select语句合并查询，查询结果显示hello、china、gauss，对括号中的select子句取limit 2
select "character_set_name" from "character_set_name" where "character_set_name"='hello'
union all (select "character_set_name" from "character_set_name" where "character_set_name"!='hello' order by "character_set_name" limit 2);

--清理环境
drop table "character_set_name";