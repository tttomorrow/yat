--  @testpoint:openGauss关键字existing(非保留)，同时作为表名和列名带引号，并进行dml操作,existing列的值最终显示为1000

drop table if exists "existing";
create table "existing"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"existing" varchar(100) default 'existing'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "existing"(c_id,"existing") values(1,'hello');
insert into "existing"(c_id,"existing") values(2,'china');
update "existing" set "existing"=1000 where "existing"='hello';
delete from "existing" where "existing"='china';
select "existing" from "existing" where "existing"!='hello' order by "existing";

drop table "existing";

