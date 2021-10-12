--  @testpoint:openGauss关键字bit_length(非保留)，作为列名带引号并且更新时使用该列，建表成功，bit_length的值更新为100
--创建表
drop table if exists bit_length_test;
create table bit_length_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"bit_length" varchar(100) default 'bit_length'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--向表中插入数据
insert into bit_length_test(c_id,"bit_length") values(1,'hello');

--更新表中数据
update bit_length_test set "bit_length"=100;

--查询表内容
select * from bit_length_test order by "bit_length";

--清理环境
drop table bit_length_test;