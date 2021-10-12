--  @testpoint:openGauss关键字role(非保留)同时作为表名和列名带引号,并使用该列结合limit排序,role列的值按字母大小排序且只显示前2条数据
--创建表
drop table if exists "role";
create table "role"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"role" varchar(100) default 'role'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--清除表数据
delete from "role";

--向保重插入数据
insert into "role"(c_id,"role") values(1,'hello');
insert into "role"(c_id,"role") values(2,'china');
insert into "role"(c_id,"role") values(3,'gauss');

--查看表内容
select "role" from "role" where "role"!='hello' order by "role" limit 2 ;

--清除环境
drop table "role";
