--  @testpoint:openGauss关键字delta(非保留)，同时作为表名和列名带引号，并进行dml操作,delta列的值最终显示为1000

drop table if exists "delta";
create table "delta"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"delta" varchar(100) default 'delta'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "delta"(c_id,"delta") values(1,'hello');
insert into "delta"(c_id,"delta") values(2,'china');
update "delta" set "delta"=1000 where "delta"='hello';
delete from "delta" where "delta"='china';
select "delta" from "delta" where "delta"!='hello' order by "delta";

drop table "delta";

