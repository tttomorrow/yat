--  @testpoint:openGauss关键字exchange(非保留)，同时作为表名和列名带引号，并进行dml操作,exchange列的值最终显示为1000

drop table if exists "exchange";
create table "exchange"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"exchange" varchar(100) default 'exchange'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "exchange"(c_id,"exchange") values(1,'hello');
insert into "exchange"(c_id,"exchange") values(2,'china');
update "exchange" set "exchange"=1000 where "exchange"='hello';
delete from "exchange" where "exchange"='china';
select "exchange" from "exchange" where "exchange"!='hello' order by "exchange";

drop table "exchange";

