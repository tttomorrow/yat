--  @testpoint:openGauss关键字percent(非保留)，作为列名带引号并且更新时使用该列，建表成功，percent的值更新为100

drop table if exists percent_test;
create table percent_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"percent" varchar(100) default 'percent'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

insert into percent_test(c_id,"percent") values(1,'hello');
update percent_test set "percent"=100;
select * from percent_test order by "percent";

drop table percent_test;