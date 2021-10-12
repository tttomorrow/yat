--  @testpoint:openGauss关键字exchange(非保留),作为列名不带引号，使用时带双引号或反引号，大小写匹配,失败

drop table if exists exchange_test;
create table exchange_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	exchange char(50)
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--插入时带双引号，插入数据成功
insert into exchange_test(c_id,"exchange") values(2,'china');
--插入时带反引号，插入数据失败
insert into exchange_test(c_id,`exchange`) values(2,'china');
select * from exchange_test;
drop table exchange_test;

