--  @testpoint:openGauss关键字delimiter(非保留)，作为列名带引号并且删除时使用该列,建表成功，delimiter列值是'hello'的删除成功

drop table if exists delimiter_test;
create table delimiter_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"delimiter" varchar(100) default 'delimiter'
) 
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

insert into delimiter_test(c_id,"delimiter") values(1,'hello');
insert into delimiter_test(c_id) values(2);
delete from delimiter_test where "delimiter"='hello';
select * from delimiter_test order by "delimiter";
drop table delimiter_test;

