--  @testpoint:openGauss关键字depth(非保留)，同时作为表名和列名带引号，并进行dml操作,depth列的值最终显示为1000

drop table if exists "depth";
create table "depth"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"depth" varchar(100) default 'depth'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "depth"(c_id,"depth") values(1,'hello');
insert into "depth"(c_id,"depth") values(2,'china');
update "depth" set "depth"=1000 where "depth"='hello';
delete from "depth" where "depth"='china';
select "depth" from "depth" where "depth"!='hello' order by "depth";

drop table "depth";

