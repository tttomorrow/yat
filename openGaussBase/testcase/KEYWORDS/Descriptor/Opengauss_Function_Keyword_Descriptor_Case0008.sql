--  @testpoint:openGauss关键字descriptor(非保留)，作为列名带引号并且删除时使用该列,建表成功，descriptor列值是'hello'的删除成功

drop table if exists descriptor_test;
create table descriptor_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"descriptor" varchar(100) default 'descriptor'
) 
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

insert into descriptor_test(c_id,"descriptor") values(1,'hello');
insert into descriptor_test(c_id) values(2);
delete from descriptor_test where "descriptor"='hello';
select * from descriptor_test order by "descriptor";
drop table descriptor_test;


