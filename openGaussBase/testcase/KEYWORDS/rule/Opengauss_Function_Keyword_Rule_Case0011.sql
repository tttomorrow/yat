--  @testpoint:openGauss关键字rule(非保留)，同时作为表名和列名带引号，并进行dml操作,rule列的值最终显示为1000

drop table if exists "rule" CASCADE;
create table "rule"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"rule" varchar(100) default 'rule'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "rule"(c_id,"rule") values(1,'hello');
insert into "rule"(c_id,"rule") values(2,'china');
update "rule" set "rule"=1000 where "rule"='hello';
delete from "rule" where "rule"='china';
select "rule" from "rule" where "rule"!='hello' order by "rule";

drop table "rule";

