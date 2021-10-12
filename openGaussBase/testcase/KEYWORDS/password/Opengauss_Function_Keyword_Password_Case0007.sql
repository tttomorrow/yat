--  @testpoint:openGauss关键字password(非保留)，作为列名带引号并且更新时使用该列，建表成功，password的值更新为100

drop table if exists password_test;
create table password_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"password" varchar(100) default 'password'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

insert into password_test(c_id,"password") values(1,'hello');
update password_test set "password"=100;
select * from password_test order by "password";

drop table password_test;