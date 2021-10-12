--  @testpoint:openGauss关键字privileges(非保留)，同时作为表名和列名带引号，并进行dml操作,privileges列的值最终显示为1000

drop table if exists "privileges";
create table "privileges"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"privileges" varchar(100) default 'privileges'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "privileges"(c_id,"privileges") values(1,'hello');
insert into "privileges"(c_id,"privileges") values(2,'china');
update "privileges" set "privileges"=1000 where "privileges"='hello';
delete from "privileges" where "privileges"='china';
select "privileges" from "privileges" where "privileges"!='hello' order by "privileges";

drop table "privileges";

