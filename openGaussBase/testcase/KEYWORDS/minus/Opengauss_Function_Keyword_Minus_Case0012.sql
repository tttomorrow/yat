--  @testpoint:openGauss保留关键字minus同时作为表名和列名带引号,并使用该列结合limit排序,minus列的值按字母大小排序且只显示前2条数据
drop table if exists "minus";
create table "minus"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"minus" varchar(100) default 'minus'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

--清理表数据
delete from "minus";

--插入数据
insert into "minus"(c_id,"minus") values(1,'hello');
insert into "minus"(c_id,"minus") values(2,'china');
insert into "minus"(c_id,"minus") values(3,'gauss');

--查看表数据
select "minus" from "minus" where "minus"!='hello' order by "minus" limit 2 ;

--清理环境
drop table "minus";