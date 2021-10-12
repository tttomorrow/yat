--  @testpoint:openGauss关键字nologging(非保留)，同时作为表名和列名带引号，并进行dml操作,nologging列的值最终显示为1000

drop table if exists "nologging";
create table "nologging"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"nologging" varchar(100) default 'nologging'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "nologging"(c_id,"nologging") values(1,'hello');
insert into "nologging"(c_id,"nologging") values(2,'china');
update "nologging" set "nologging"=1000 where "nologging"='hello';
delete from "nologging" where "nologging"='china';
select "nologging" from "nologging" where "nologging"!='hello' order by "nologging";

drop table "nologging";

