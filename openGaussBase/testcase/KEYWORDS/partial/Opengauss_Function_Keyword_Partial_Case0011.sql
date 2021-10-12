--  @testpoint:openGauss关键字partial(非保留)，同时作为表名和列名带引号，并进行dml操作,partial列的值最终显示为1000

drop table if exists "partial";
create table "partial"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"partial" varchar(100) default 'partial'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "partial"(c_id,"partial") values(1,'hello');
insert into "partial"(c_id,"partial") values(2,'china');
update "partial" set "partial"=1000 where "partial"='hello';
delete from "partial" where "partial"='china';
select "partial" from "partial" where "partial"!='hello' order by "partial";

drop table "partial";
