--  @testpoint:openGauss关键字unlimited(非保留)，同时作为表名和列名带引号，并进行dml操作,unlimited列的值最终显示为1000

drop table if exists "unlimited" CASCADE;
create table "unlimited"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"unlimited" varchar(100) default 'unlimited'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "unlimited"(c_id,"unlimited") values(1,'hello');
insert into "unlimited"(c_id,"unlimited") values(2,'china');
update "unlimited" set "unlimited"=1000 where "unlimited"='hello';
delete from "unlimited" where "unlimited"='china';
select "unlimited" from "unlimited" where "unlimited"!='hello' order by "unlimited";

drop table "unlimited";

