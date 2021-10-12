--  @testpoint:openGauss关键字reads(非保留)，作为列名带引号并且删除时使用该列,建表成功，reads列值是'hello'的删除成功

drop table if exists reads_test;
create table reads_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"reads" varchar(100) default 'reads'
) 
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

insert into reads_test(c_id,"reads") values(1,'hello');
insert into reads_test(c_id) values(2);
delete from reads_test where "reads"='hello';
select * from reads_test order by "reads";
drop table reads_test;


