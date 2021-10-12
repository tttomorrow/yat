--  @testpoint:openGauss关键字bit_length(非保留)，同时作为表名和列名带引号，与union结合查询合并两个SELECT 语句查询
--创建表
drop table if exists "bit_length";
create table "bit_length"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"bit_length" varchar(100) default 'bit_length'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--向表中插入数据
insert into "bit_length"(c_id,"bit_length") values(1,'hello');
insert into "bit_length"(c_id,"bit_length") values(2,'china');
insert into "bit_length"(c_id,"bit_length") values(3,'gauss');

---两个select语句合并查询，查询结果显示hello、china、gauss，对括号中的select子句取limit 2
select "bit_length" from "bit_length" where "bit_length"='hello'
union all (select "bit_length" from "bit_length" where "bit_length"!='hello' order by "bit_length" limit 2);

--清理环境
drop table "bit_length";