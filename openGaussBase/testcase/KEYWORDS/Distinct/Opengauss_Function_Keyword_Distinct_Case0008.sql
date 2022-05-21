--  @testpoint:openGauss保留关键字distinct作为列名带引号并且删除时使用该列,建表成功，distinct列值是'hello'的删除成功
drop table if exists zsharding_tbl;
create table zsharding_tbl(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"distinct" varchar(100) default 'distinct'
) 
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

insert into zsharding_tbl(c_id,"distinct") values(1,'hello');
insert into zsharding_tbl(c_id) values(2);
delete from zsharding_tbl where "distinct"='hello';
select * from zsharding_tbl order by "distinct";
drop table zsharding_tbl;


