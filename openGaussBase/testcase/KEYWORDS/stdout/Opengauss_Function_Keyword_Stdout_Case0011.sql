--  @testpoint:openGauss关键字stdout(非保留)，同时作为表名和列名带引号，并进行dml操作,stdout列的值最终显示为1000

drop table if exists "stdout" CASCADE;
create table "stdout"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"stdout" varchar(100) default 'stdout'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "stdout"(c_id,"stdout") values(1,'hello');
insert into "stdout"(c_id,"stdout") values(2,'china');
update "stdout" set "stdout"=1000 where "stdout"='hello';
delete from "stdout" where "stdout"='china';
select "stdout" from "stdout" where "stdout"!='hello' order by "stdout";

drop table "stdout";

