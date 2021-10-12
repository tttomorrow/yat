--  @testpoint:openGauss保留关键字unique作为列名带引号并且删除时使用该列,建表成功，unique列值是'hello'的删除成功
drop table if exists unique_test;
create table unique_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"unique" varchar(100) default 'unique'
) 
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

insert into unique_test(c_id,"unique") values(1,'hello');
insert into unique_test(c_id) values(2);
delete from unique_test where "unique"='hello';
select * from unique_test order by "unique";
drop table unique_test;


