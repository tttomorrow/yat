--  @testpoint:openGauss关键字distribution(非保留)，作为列名带引号并且排序时使用该列,建表成功，distribution列按字母大小排序

drop table if exists distribution_test;
create table distribution_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"distribution" varchar(100) default 'distribution'
) 
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

insert into distribution_test(c_id,"distribution") values(1,'hello');
select * from distribution_test order by "distribution";
drop table distribution_test;

