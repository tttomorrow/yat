--  @testpoint:openGauss关键字returned_octet_length(非保留)同时作为表名和列名带引号,并使用该列结合limit排序,returned_octet_length列的值按字母大小排序且只显示前2条数据

drop table if exists "returned_octet_length";
create table "returned_octet_length"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"returned_octet_length" varchar(100) default 'returned_octet_length'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
delete from "returned_octet_length";
insert into "returned_octet_length"(c_id,"returned_octet_length") values(1,'hello');
insert into "returned_octet_length"(c_id,"returned_octet_length") values(2,'china');
insert into "returned_octet_length"(c_id,"returned_octet_length") values(3,'gauss');
select "returned_octet_length" from "returned_octet_length" where "returned_octet_length"!='hello' order by "returned_octet_length" limit 2 ;

drop table "returned_octet_length";

