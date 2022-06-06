--  @testpoint:openGauss关键字result(非保留)，作为列名带引号并且更新时使用该列，建表成功，result的值更新为100

drop table if exists result_test;
create table result_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"result" varchar(100) default 'result'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

insert into result_test(c_id,"result") values(1,'hello');
update result_test set "result"=100;
select * from result_test order by "result";

drop table result_test;