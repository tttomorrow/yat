--  @testpoint:openGauss关键字prepare(非保留)同时作为表名和列名带引号,并使用该列结合limit排序,prepare列的值按字母大小排序且只显示前2条数据

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
	partition P_max values less than (maxvalue)
);
delete from "prepare";
insert into "prepare"(c_id,"prepare") values(1,'hello');
insert into "prepare"(c_id,"prepare") values(2,'china');
insert into "prepare"(c_id,"prepare") values(3,'gauss');
select "prepare" from "prepare" where "prepare"!='hello' order by "prepare" limit 2 ;

drop table "prepare";

