--  @testpoint:openGauss保留关键字freeze作为列名带引号并且删除时使用该列,建表成功，freeze列值是'hello'的删除成功
drop table if exists test_tbl;
create table test_tbl(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"freeze" varchar(100) default 'freeze'
) 
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--插入数据
insert into test_tbl(c_id,"freeze") values(1,'hello');
insert into test_tbl(c_id) values(2);

--查看表数据
select c_id,"freeze" from test_tbl;

--删除表数据
delete from test_tbl where "freeze"='hello';

--查看表数据
select c_id,"freeze" from test_tbl;

--清理环境
drop table test_tbl;


