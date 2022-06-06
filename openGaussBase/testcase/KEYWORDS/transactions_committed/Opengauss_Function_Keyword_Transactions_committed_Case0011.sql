--  @testpoint:openGauss关键字transactions_committed(非保留)，同时作为表名和列名带引号，并进行dml操作,transactions_committed列的值最终显示为1000

drop table if exists "transactions_committed" CASCADE;
create table "transactions_committed"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"transactions_committed" varchar(100) default 'transactions_committed'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "transactions_committed"(c_id,"transactions_committed") values(1,'hello');
insert into "transactions_committed"(c_id,"transactions_committed") values(2,'china');
update "transactions_committed" set "transactions_committed"=1000 where "transactions_committed"='hello';
delete from "transactions_committed" where "transactions_committed"='china';
select "transactions_committed" from "transactions_committed" where "transactions_committed"!='hello' order by "transactions_committed";

drop table "transactions_committed";

