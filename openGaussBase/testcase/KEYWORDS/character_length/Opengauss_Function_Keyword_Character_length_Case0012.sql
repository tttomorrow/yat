--  @testpoint:openGauss关键字character_length(非保留)同时作为表名和列名带引号,并使用该列结合limit排序,character_length列的值按字母大小排序且只显示前2条数据
--创建表
drop table if exists "character_length";
create table "character_length"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"character_length" varchar(100) default 'character_length'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

--清除表数据
delete from "character_length";

--向保重插入数据
insert into "character_length"(c_id,"character_length") values(1,'hello');
insert into "character_length"(c_id,"character_length") values(2,'china');
insert into "character_length"(c_id,"character_length") values(3,'gauss');

--查看表内容
select "character_length" from "character_length" where "character_length"!='hello' order by "character_length" limit 2 ;

--清除环境
drop table "character_length";
