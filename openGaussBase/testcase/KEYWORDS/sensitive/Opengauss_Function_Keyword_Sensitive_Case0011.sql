--  @testpoint:openGauss关键字sensitive(非保留)，同时作为表名和列名带引号，并进行dml操作,sensitive列的值最终显示为1000

drop table if exists "sensitive" CASCADE;
create table "sensitive"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"sensitive" varchar(100) default 'sensitive'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "sensitive"(c_id,"sensitive") values(1,'hello');
insert into "sensitive"(c_id,"sensitive") values(2,'china');
update "sensitive" set "sensitive"=1000 where "sensitive"='hello';
delete from "sensitive" where "sensitive"='china';
select "sensitive" from "sensitive" where "sensitive"!='hello' order by "sensitive";

drop table "sensitive";

