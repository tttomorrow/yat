--  @testpoint:openGauss关键字lower(非保留)，同时作为表名和列名带引号，并进行dml操作,lower列的值最终显示为1000

drop table if exists "lower";
create table "lower"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"lower" varchar(100) default 'lower'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "lower"(c_id,"lower") values(1,'hello');
insert into "lower"(c_id,"lower") values(2,'china');
update "lower" set "lower"=1000 where "lower"='hello';
delete from "lower" where "lower"='china';
select "lower" from "lower" where "lower"!='hello' order by "lower";

drop table "lower";

