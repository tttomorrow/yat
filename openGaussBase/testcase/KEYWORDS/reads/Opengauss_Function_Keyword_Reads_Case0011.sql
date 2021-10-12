--  @testpoint:openGauss关键字reads(非保留)，同时作为表名和列名带引号，并进行dml操作,reads列的值最终显示为1000

drop table if exists "reads";
create table "reads"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"reads" varchar(100) default 'reads'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "reads"(c_id,"reads") values(1,'hello');
insert into "reads"(c_id,"reads") values(2,'china');
update "reads" set "reads"=1000 where "reads"='hello';
delete from "reads" where "reads"='china';
select "reads" from "reads" where "reads"!='hello' order by "reads";

drop table "reads";

