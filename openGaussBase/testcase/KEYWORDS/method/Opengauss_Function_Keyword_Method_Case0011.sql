--  @testpoint:openGauss关键字method(非保留)，同时作为表名和列名带引号，并进行dml操作,method列的值最终显示为1000

drop table if exists "method";
create table "method"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"method" varchar(100) default 'method'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "method"(c_id,"method") values(1,'hello');
insert into "method"(c_id,"method") values(2,'china');
update "method" set "method"=1000 where "method"='hello';
delete from "method" where "method"='china';
select "method" from "method" where "method"!='hello' order by "method";

drop table "method";

