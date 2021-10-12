--  @testpoint:openGauss关键字returned_octet_length(非保留)，作为列名带引号并且更新时使用该列，建表成功，returned_octet_length的值更新为100

drop table if exists returned_octet_length_test;
create table returned_octet_length_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"returned_octet_length" varchar(100) default 'returned_octet_length'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

insert into returned_octet_length_test(c_id,"returned_octet_length") values(1,'hello');
update returned_octet_length_test set "returned_octet_length"=100;
select * from returned_octet_length_test order by "returned_octet_length";

drop table returned_octet_length_test;