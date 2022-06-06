--  @testpoint:openGauss保留关键字 session_user 作为列名带引号并且更新时使用该列，建表成功，session_user的值更新为100
drop table if exists test_tbl;
create table test_tbl(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"session_user" varchar(100) default 'session_user'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

--插入数据
insert into test_tbl(c_id,"session_user") values(1,'hello');
insert into test_tbl(c_id) values(2);

--查询表数据
select c_id,"session_user" from test_tbl;

--更新表数据
update test_tbl set "session_user"=100;

--查询表数据
select c_id,"session_user" from test_tbl;

--清理环境
drop table test_tbl;