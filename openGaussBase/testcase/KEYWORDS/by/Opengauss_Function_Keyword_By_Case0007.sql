--  @testpoint:openGauss关键字by(非保留)，作为列名带引号并且更新时使用该列，建表成功，by的值更新为100
--创建表
drop table if exists by_test;
create table by_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"by" varchar(100) default 'by'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--向表中插入数据
insert into by_test(c_id,"by") values(1,'hello');

--更新表中数据
update by_test set "by"=100;

--查询表内容
select * from by_test order by "by";

--清理环境
drop table by_test;