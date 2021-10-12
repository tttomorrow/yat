--  @testpoint:openGauss关键字destroy(非保留)，作为列名带引号并且删除时使用该列,建表成功，destroy列值是'hello'的删除成功

drop table if exists destroy_test;
create table destroy_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"destroy" varchar(100) default 'destroy'
) 
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

insert into destroy_test(c_id,"destroy") values(1,'hello');
insert into destroy_test(c_id) values(2);
delete from destroy_test where "destroy"='hello';
select * from destroy_test order by "destroy";
drop table destroy_test;


