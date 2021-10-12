--  @testpoint:openGauss关键字date(非保留)，作为列名带引号并且删除时使用该列,建表成功，date列值是'hello'的删除成功

drop table if exists date_test;
create table date_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"date" varchar(100) default 'date'
) 
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

insert into date_test(c_id,"date") values(1,'hello');
insert into date_test(c_id) values(2);
delete from date_test where "date"='hello';
select * from date_test order by "date";
drop table date_test;


