--  @testpoint:openGauss保留关键字unique同时作为表名和列名带引号,并使用该列结合limit排序,unique列的值按字母大小排序且只显示前2条数据
drop table if exists "unique";
create table "unique"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"unique" varchar(100) default 'unique'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
delete from "unique";
insert into "unique"(c_id,"unique") values(1,'hello');
insert into "unique"(c_id,"unique") values(2,'china');
insert into "unique"(c_id,"unique") values(3,'gauss');
select "unique" from "unique" where "unique"!='hello' order by "unique" limit 2 ;

drop table "unique";