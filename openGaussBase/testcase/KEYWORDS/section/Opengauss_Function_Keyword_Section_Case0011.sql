--  @testpoint:openGauss关键字section(非保留)，同时作为表名和列名带引号，并进行dml操作,section列的值最终显示为1000

drop table if exists "section" CASCADE;
create table "section"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"section" varchar(100) default 'section'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "section"(c_id,"section") values(1,'hello');
insert into "section"(c_id,"section") values(2,'china');
update "section" set "section"=1000 where "section"='hello';
delete from "section" where "section"='china';
select "section" from "section" where "section"!='hello' order by "section";

drop table "section";

