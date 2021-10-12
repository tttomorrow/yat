--  @testpoint:openGauss关键字dictionary(非保留)同时作为表名和列名带引号,并使用该列结合limit排序,dictionary列的值按字母大小排序且只显示前2条数据

drop table if exists "dictionary";
create table "dictionary"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"dictionary" varchar(100) default 'dictionary'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
delete from "dictionary";
insert into "dictionary"(c_id,"dictionary") values(1,'hello');
insert into "dictionary"(c_id,"dictionary") values(2,'china');
insert into "dictionary"(c_id,"dictionary") values(3,'gauss');
select "dictionary" from "dictionary" where "dictionary"!='hello' order by "dictionary" limit 2 ;

drop table "dictionary";

