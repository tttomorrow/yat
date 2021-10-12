--  @testpoint:openGauss关键字uncommitted(非保留)，同时作为表名和列名带引号，并进行dml操作,uncommitted列的值最终显示为1000

drop table if exists "uncommitted" CASCADE;
create table "uncommitted"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"uncommitted" varchar(100) default 'uncommitted'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "uncommitted"(c_id,"uncommitted") values(1,'hello');
insert into "uncommitted"(c_id,"uncommitted") values(2,'china');
update "uncommitted" set "uncommitted"=1000 where "uncommitted"='hello';
delete from "uncommitted" where "uncommitted"='china';
select "uncommitted" from "uncommitted" where "uncommitted"!='hello' order by "uncommitted";

drop table "uncommitted";

