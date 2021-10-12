--  @testpoint:openGauss关键字add(非保留)同时作为表名和列名带引号,并使用该列结合limit排序,add列的值按字母大小排序且只显示前2条数据
--创建表
drop table if exists "add";
create table "add"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"add" varchar(100) default 'add'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--清除表数据
delete from "add";

--向保重插入数据
insert into "add"(c_id,"add") values(1,'hello');
insert into "add"(c_id,"add") values(2,'china');
insert into "add"(c_id,"add") values(3,'gauss');

--查看表内容
select "add" from "add" where "add"!='hello' order by "add" limit 2 ;

--清除环境
drop table "add";