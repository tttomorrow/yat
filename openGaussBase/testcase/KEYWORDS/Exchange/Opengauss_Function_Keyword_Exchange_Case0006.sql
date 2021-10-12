--  @testpoint:openGauss关键字exchange(非保留),作为列名带引号并且插入时使用该列，建表成功，给该列插入数据成功

drop table if exists exchange_test;
create table exchange_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"exchange" varchar(20) default 'gauss'
) 
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
insert into exchange_test(c_id,"exchange") values(1,'hello');
select * from exchange_test order by 1;

drop table exchange_test;