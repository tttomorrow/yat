--  @testpoint:openGauss关键字Including(非保留)，同时作为表名和列名带引号，并进行dml操作,Including列的值最终显示为1000

drop table if exists "Including";
create table "Including"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Including" varchar(100) default 'Including'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "Including"(c_id,"Including") values(1,'hello');
insert into "Including"(c_id,"Including") values(2,'china');
update "Including" set "Including"=1000 where "Including"='hello';
delete from "Including" where "Including"='china';
select "Including" from "Including" where "Including"!='hello' order by "Including";

drop table "Including";

