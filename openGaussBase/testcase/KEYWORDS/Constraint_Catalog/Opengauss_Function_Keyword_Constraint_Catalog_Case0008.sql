--  @testpoint:openGauss关键字constraint_catalog(非保留)，作为列名带引号并且删除时使用该列,建表成功，constraint_catalog列值是'hello'的删除成功

drop table if exists constraint_catalog_test;
create table constraint_catalog_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"constraint_catalog" varchar(100) default 'constraint_catalog'
) 
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

insert into constraint_catalog_test(c_id,"constraint_catalog") values(1,'hello');
insert into constraint_catalog_test(c_id) values(2);
delete from constraint_catalog_test where "constraint_catalog"='hello';
select * from constraint_catalog_test order by "constraint_catalog";
drop table constraint_catalog_test;


