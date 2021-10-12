--  @testpoint:openGauss关键字access(非保留)，同时作为表名和列名带引号，与union结合查询合并两个SELECT 语句查询
--创建表
drop table if exists "access";
create table "access"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"access" varchar(100) default 'access'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--向表中插入数据
insert into "access"(c_id,"access") values(1,'hello');
insert into "access"(c_id,"access") values(2,'china');
insert into "access"(c_id,"access") values(3,'gauss');

---两个select语句合并查询，查询结果显示hello、china、gauss，对括号中的select子句取limit 2
select "access" from "access" where "access"='hello'
union all (select "access" from "access" where "access"!='hello' order by "access" limit 2);

--清理环境
drop table "access";