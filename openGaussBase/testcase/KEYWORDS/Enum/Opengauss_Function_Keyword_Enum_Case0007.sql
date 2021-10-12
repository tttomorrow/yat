--  @testpoint:openGauss关键字enum(非保留)，作为列名带引号并且更新时使用该列，建表成功，enum的值更新为100

drop table if exists enum_test;
create table enum_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"enum" varchar(100) default 'enum'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

insert into enum_test(c_id,"enum") values(1,'hello');
update enum_test set "enum"=100;
select * from enum_test order by "enum";

drop table enum_test;