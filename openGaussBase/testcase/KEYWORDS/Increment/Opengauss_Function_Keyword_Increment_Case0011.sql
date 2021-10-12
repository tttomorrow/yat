--  @testpoint:openGauss关键字Increment(非保留)，同时作为表名和列名带引号，并进行dml操作,Increment列的值最终显示为1000

drop table if exists "Increment";
create table "Increment"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Increment" varchar(100) default 'Increment'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "Increment"(c_id,"Increment") values(1,'hello');
insert into "Increment"(c_id,"Increment") values(2,'china');
update "Increment" set "Increment"=1000 where "Increment"='hello';
delete from "Increment" where "Increment"='china';
select "Increment" from "Increment" where "Increment"!='hello' order by "Increment";

drop table "Increment";

