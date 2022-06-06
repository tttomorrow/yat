--  @testpoint:openGauss关键字deferred(非保留)，作为列名带引号并且删除时使用该列,建表成功，deferred列值是'hello'的删除成功

drop table if exists deferred_test;
create table deferred_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"deferred" varchar(100) default 'deferred'
) 
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

insert into deferred_test(c_id,"deferred") values(1,'hello');
insert into deferred_test(c_id) values(2);
delete from deferred_test where "deferred"='hello';
select * from deferred_test order by "deferred";
drop table deferred_test;


