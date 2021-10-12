--  @testpoint:openGauss关键字Label(非保留)同时作为表名和列名带引号,并使用该列结合limit排序,Label列的值按字母大小排序且只显示前2条数据

drop table if exists "explain";
create table "explain"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"explain" varchar(100) default 'explain'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
delete from "explain";
insert into "explain"(c_id,"explain") values(1,'hello');
insert into "explain"(c_id,"explain") values(2,'china');
insert into "explain"(c_id,"explain") values(3,'gauss');
select "explain" from "explain" where "explain"!='hello' order by "explain" limit 2 ;

drop table "explain";

