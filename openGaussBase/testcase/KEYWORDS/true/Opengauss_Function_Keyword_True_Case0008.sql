--  @testpoint:openGauss保留关键字true作为列名带引号并且删除时使用该列,建表成功，true列值是'hello'的删除成功
drop table if exists true_test;
create table true_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"true" varchar(100) default 'true'
) 
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

insert into true_test(c_id,"true") values(1,'hello');
insert into true_test(c_id) values(2);
delete from true_test where "true"='hello';
select * from true_test order by "true";
drop table true_test;


