--  @testpoint:openGauss关键字fixed(非保留)，作为列名带引号并且删除时使用该列,建表成功，fixed列值是'hello'的删除成功

drop table if exists fixed_test;
create table fixed_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"fixed" varchar(100) default 'fixed'
) 
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

insert into fixed_test(c_id,"fixed") values(1,'hello');
insert into fixed_test(c_id) values(2);
delete from fixed_test where "fixed"='hello';
select * from fixed_test order by "fixed";
drop table fixed_test;


