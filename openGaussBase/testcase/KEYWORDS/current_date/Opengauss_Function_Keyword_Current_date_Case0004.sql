-- @testpoint: openGauss保留关键字 current_date 作为列名带双引号，使用时带单引号或反引号，大小写匹配，部分测试点合理报错

drop table if exists test_tbl;
create table test_tbl(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	“current_date” char(50)
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--插入数据
insert into test_tbl(c_id,'current_date') values(2,'china');
insert into test_tbl(c_id,`current_date`) values(2,'china');
drop table if exists test_tbl;

