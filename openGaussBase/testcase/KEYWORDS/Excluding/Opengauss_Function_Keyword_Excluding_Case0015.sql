--  @testpoint:openGauss关键字excluding(非保留),作为列名带双引号，使用时不带,插入成功

drop table if exists excluding_test;
create table excluding_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"excluding" char(50)	
) 
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
insert into excluding_test(c_id,excluding) values(2,'china');
select * from excluding_test;
drop table excluding_test;