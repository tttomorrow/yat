--  @testpoint:openGauss关键字module(非保留)，同时作为表名和列名带引号，并进行dml操作,module列的值最终显示为1000

drop table if exists "module";
create table "module"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"module" varchar(100) default 'module'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "module"(c_id,"module") values(1,'hello');
insert into "module"(c_id,"module") values(2,'china');
update "module" set "module"=1000 where "module"='hello';
delete from "module" where "module"='china';
select "module" from "module" where "module"!='hello' order by "module";

drop table "module";

