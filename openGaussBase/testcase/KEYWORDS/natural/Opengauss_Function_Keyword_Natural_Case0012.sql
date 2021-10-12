--  @testpoint:openGauss保留关键字natural同时作为表名和列名带引号,并使用该列结合limit排序,natural列的值按字母大小排序且只显示前2条数据
drop table if exists "natural";
create table "natural"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"natural" varchar(100) default 'natural'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--清理表数据
delete from "natural";

--插入数据
insert into "natural"(c_id,"natural") values(1,'hello');
insert into "natural"(c_id,"natural") values(2,'china');
insert into "natural"(c_id,"natural") values(3,'gauss');

--查看表数据
select "natural" from "natural" where "natural"!='hello' order by "natural" limit 2 ;

--清理环境
drop table "natural";