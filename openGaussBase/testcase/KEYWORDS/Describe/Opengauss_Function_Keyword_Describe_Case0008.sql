--  @testpoint:openGauss关键字describe(非保留)，作为列名带引号并且删除时使用该列,建表成功，describe列值是'hello'的删除成功

drop table if exists describe_test;
create table describe_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"describe" varchar(100) default 'describe'
) 
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

insert into describe_test(c_id,"describe") values(1,'hello');
insert into describe_test(c_id) values(2);
delete from describe_test where "describe"='hello';
select * from describe_test order by "describe";
drop table describe_test;


