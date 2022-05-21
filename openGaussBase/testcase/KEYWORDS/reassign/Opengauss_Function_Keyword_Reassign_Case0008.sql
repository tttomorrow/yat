--  @testpoint:openGauss关键字reassign(非保留)，作为列名带引号并且删除时使用该列,建表成功，reassign列值是'hello'的删除成功

drop table if exists reassign_test;
create table reassign_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"reassign" varchar(100) default 'reassign'
) 
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

insert into reassign_test(c_id,"reassign") values(1,'hello');
insert into reassign_test(c_id) values(2);
delete from reassign_test where "reassign"='hello';
select * from reassign_test order by "reassign";
drop table reassign_test;


