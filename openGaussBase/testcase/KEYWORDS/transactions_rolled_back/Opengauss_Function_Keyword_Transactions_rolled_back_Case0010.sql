--  @testpoint:openGauss关键字transactions_rolled_back(非保留),同时作为表名和列名带引号，建表成功

drop table if exists "transactions_rolled_back" CASCADE;
create table "transactions_rolled_back"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"transactions_rolled_back" varchar(100) default 'transactions_rolled_back'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);
select * from "transactions_rolled_back";
drop table "transactions_rolled_back" CASCADE;

