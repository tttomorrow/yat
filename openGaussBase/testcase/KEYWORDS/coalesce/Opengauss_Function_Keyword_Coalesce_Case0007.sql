--  @testpoint:openGauss关键字coalesce(非保留)，作为列名带引号并且更新时使用该列，建表成功，coalesce的值更新为100
--创建表
drop table if exists coalesce_test;
create table coalesce_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"coalesce" varchar(100) default 'coalesce'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--向表中插入数据
insert into coalesce_test(c_id,"coalesce") values(1,'hello');

--更新表中数据
update coalesce_test set "coalesce"=100;

--查询表内容
select * from coalesce_test order by "coalesce";

--清理环境
drop table coalesce_test;