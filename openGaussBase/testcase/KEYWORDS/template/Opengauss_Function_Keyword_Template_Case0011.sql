--  @testpoint:openGauss关键字template(非保留)，同时作为表名和列名带引号，并进行dml操作,template列的值最终显示为1000

drop table if exists "template" CASCADE;
create table "template"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"template" varchar(100) default 'template'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "template"(c_id,"template") values(1,'hello');
insert into "template"(c_id,"template") values(2,'china');
update "template" set "template"=1000 where "template"='hello';
delete from "template" where "template"='china';
select "template" from "template" where "template"!='hello' order by "template";

drop table "template";

