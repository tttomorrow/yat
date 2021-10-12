--  @testpoint:openGauss关键字view(非保留)，同时作为表名和列名带引号，并进行dml操作,view列的值最终显示为1000

drop table if exists "view";
create table "view"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"view" varchar(100) default 'view'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "view"(c_id,"view") values(1,'hello');
insert into "view"(c_id,"view") values(2,'china');
update "view" set "view"=1000 where "view"='hello';
delete from "view" where "view"='china';
select "view" from "view" where "view"!='hello' order by "view";

drop table "view";

