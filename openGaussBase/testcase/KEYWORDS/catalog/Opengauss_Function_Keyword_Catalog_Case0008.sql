--  @testpoint:openGauss关键字catalog(非保留)，作为列名带引号并且删除时使用该列,建表成功，catalog列值是'hello'的删除成功
--创建表
drop table if exists catalog_test;
create table catalog_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"catalog" varchar(100) default 'catalog'
) 
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

--向表中插入数据
insert into catalog_test(c_id,"catalog") values(1,'hello');

--查询表内容
select * from catalog_test;

--向表中插入数据
insert into catalog_test(c_id) values(2);

--删除表数据
delete from catalog_test where "catalog"='hello';

--查询表内容
select * from catalog_test order by "catalog";

--清理环境
drop table catalog_test;
