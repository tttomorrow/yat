--  @testpoint:openGauss关键字Ignore(非保留)，同时作为表名和列名带引号，并进行dml操作,Ignore列的值最终显示为1000

drop table if exists "Ignore";
create table "Ignore"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Ignore" varchar(100) default 'Ignore'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "Ignore"(c_id,"Ignore") values(1,'hello');
insert into "Ignore"(c_id,"Ignore") values(2,'china');
update "Ignore" set "Ignore"=1000 where "Ignore"='hello';
delete from "Ignore" where "Ignore"='china';
select "Ignore" from "Ignore" where "Ignore"!='hello' order by "Ignore";

drop table "Ignore";

