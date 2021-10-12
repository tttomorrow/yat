--  @testpoint:openGauss关键字translate(非保留)，同时作为表名和列名带引号，并进行dml操作,translate列的值最终显示为1000

drop table if exists "translate" CASCADE;
create table "translate"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"translate" varchar(100) default 'translate'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "translate"(c_id,"translate") values(1,'hello');
insert into "translate"(c_id,"translate") values(2,'china');
update "translate" set "translate"=1000 where "translate"='hello';
delete from "translate" where "translate"='china';
select "translate" from "translate" where "translate"!='hello' order by "translate";

drop table "translate";

