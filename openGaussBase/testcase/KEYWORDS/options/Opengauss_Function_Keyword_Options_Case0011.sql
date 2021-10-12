--  @testpoint:openGauss关键字options(非保留)，同时作为表名和列名带引号，并进行dml操作,options列的值最终显示为1000

drop table if exists "options";
create table "options"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"options" varchar(100) default 'options'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "options"(c_id,"options") values(1,'hello');
insert into "options"(c_id,"options") values(2,'china');
update "options" set "options"=1000 where "options"='hello';
delete from "options" where "options"='china';
select "options" from "options" where "options"!='hello' order by "options";

drop table "options";

