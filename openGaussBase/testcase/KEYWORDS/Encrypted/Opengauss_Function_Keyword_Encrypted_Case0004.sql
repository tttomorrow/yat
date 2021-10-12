--  @testpoint:openGauss关键字encrypted(非保留),作为列名不带引号，使用时带双引号或反引号，大小写匹配,失败

drop table if exists encrypted_test;
create table encrypted_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	encrypted char(50)
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--插入时带带引号，插入数据成功
insert into encrypted_test(c_id,"encrypted") values(2,'china');
--插入时带反引号，插入数据失败
insert into encrypted_test(c_id,`encrypted`) values(2,'china');
select * from encrypted_test;
drop table encrypted_test;

