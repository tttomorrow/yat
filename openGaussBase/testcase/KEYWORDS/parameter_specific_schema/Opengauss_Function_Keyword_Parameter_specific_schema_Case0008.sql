--  @testpoint:openGauss关键字parameter_specific_schema(非保留)，作为列名带引号并且删除时使用该列,建表成功，parameter_specific_schema列值是'hello'的删除成功

drop table if exists explain_test;
create table explain_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"parameter_specific_schema" varchar(100) default 'parameter_specific_schema'
) 
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

insert into explain_test(c_id,"parameter_specific_schema") values(1,'hello');
insert into explain_test(c_id) values(2);
delete from explain_test where "parameter_specific_schema"='hello';
select * from explain_test order by "parameter_specific_schema";
drop table explain_test;


