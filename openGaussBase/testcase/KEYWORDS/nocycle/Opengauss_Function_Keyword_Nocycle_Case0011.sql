--  @testpoint:openGauss关键字nocycle(非保留)，同时作为表名和列名带引号，并进行dml操作,nocycle列的值最终显示为1000

drop table if exists "nocycle";
create table "nocycle"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"nocycle" varchar(100) default 'nocycle'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "nocycle"(c_id,"nocycle") values(1,'hello');
insert into "nocycle"(c_id,"nocycle") values(2,'china');
update "nocycle" set "nocycle"=1000 where "nocycle"='hello';
delete from "nocycle" where "nocycle"='china';
select "nocycle" from "nocycle" where "nocycle"!='hello' order by "nocycle";

drop table "nocycle";

