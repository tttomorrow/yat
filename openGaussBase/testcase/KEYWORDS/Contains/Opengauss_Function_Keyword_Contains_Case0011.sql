--  @testpoint:openGauss关键字contains(非保留)，同时作为表名和列名带引号，并进行dml操作,contains列的值最终显示为1000

drop table if exists "contains";
create table "contains"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"contains" varchar(100) default 'contains'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "contains"(c_id,"contains") values(1,'hello');
insert into "contains"(c_id,"contains") values(2,'china');
update "contains" set "contains"=1000 where "contains"='hello';
delete from "contains" where "contains"='china';
select "contains" from "contains" where "contains"!='hello' order by "contains";

drop table "contains";

