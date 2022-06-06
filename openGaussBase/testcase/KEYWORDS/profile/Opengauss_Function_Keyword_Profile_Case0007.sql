--  @testpoint:openGauss关键字profile(非保留)，作为列名带引号并且更新时使用该列，建表成功，profile的值更新为100

drop table if exists profile_test;
create table profile_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"profile" varchar(100) default 'profile'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

insert into profile_test(c_id,"profile") values(1,'hello');
update profile_test set "profile"=100;
select * from profile_test order by "profile";

drop table profile_test;