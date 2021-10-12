--  @testpoint:openGauss关键字sqlexception(非保留)，同时作为表名和列名带引号，并进行dml操作,sqlexception列的值最终显示为1000

drop table if exists "sqlexception" CASCADE;
create table "sqlexception"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"sqlexception" varchar(100) default 'sqlexception'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "sqlexception"(c_id,"sqlexception") values(1,'hello');
insert into "sqlexception"(c_id,"sqlexception") values(2,'china');
update "sqlexception" set "sqlexception"=1000 where "sqlexception"='hello';
delete from "sqlexception" where "sqlexception"='china';
select "sqlexception" from "sqlexception" where "sqlexception"!='hello' order by "sqlexception";

drop table "sqlexception";

