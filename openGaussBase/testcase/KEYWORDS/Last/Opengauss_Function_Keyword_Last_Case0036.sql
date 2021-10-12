-- @testpoint: openGauss关键字Last(非保留),创建游标，用last抓取最后一行数据

drop table if exists Explain_test;
create table Explain_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	Last text
);

START TRANSACTION;

CURSOR cursor1 FOR SELECT * FROM Explain_test;

FETCH last  FROM cursor1;

CLOSE cursor1;

end;
--清理环境
drop table if exists Explain_test cascade;



