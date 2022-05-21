--  @testpoint:openGauss关键字prepare(非保留)，同时作为表名和列名带引号，与union结合查询合并两个SELECT 语句查询

drop table if exists "prepare";
create table "prepare"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"prepare" varchar(100) default 'prepare'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

insert into "prepare"(c_id,"prepare") values(1,'hello');
insert into "prepare"(c_id,"prepare") values(2,'china');
insert into "prepare"(c_id,"prepare") values(3,'gauss');

---两个select语句合并查询，查询结果显示hello、china、gauss，对括号中的select子句取limit 2
select "prepare" from "prepare" where "prepare"='hello'
union all (select "prepare" from "prepare" where "prepare"!='hello' order by "prepare" limit 2);

drop table "prepare";