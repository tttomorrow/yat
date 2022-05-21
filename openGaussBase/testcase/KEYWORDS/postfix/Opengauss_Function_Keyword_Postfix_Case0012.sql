--  @testpoint:openGauss关键字postfix(非保留)同时作为表名和列名带引号,并使用该列结合limit排序,postfix列的值按字母大小排序且只显示前2条数据

drop table if exists "postfix";
create table "postfix"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"postfix" varchar(100) default 'postfix'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);
delete from "postfix";
insert into "postfix"(c_id,"postfix") values(1,'hello');
insert into "postfix"(c_id,"postfix") values(2,'china');
insert into "postfix"(c_id,"postfix") values(3,'gauss');
select "postfix" from "postfix" where "postfix"!='hello' order by "postfix" limit 2 ;

drop table "postfix";

