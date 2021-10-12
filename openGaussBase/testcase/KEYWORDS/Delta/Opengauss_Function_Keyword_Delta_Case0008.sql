--  @testpoint:openGauss关键字delta(非保留)，作为列名带引号并且删除时使用该列,建表成功，delta列值是'hello'的删除成功

drop table if exists delta_test;
create table delta_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"delta" varchar(100) default 'delta'
) 
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

insert into delta_test(c_id,"delta") values(1,'hello');
insert into delta_test(c_id) values(2);
delete from delta_test where "delta"='hello';
select * from delta_test order by "delta";
drop table delta_test;


