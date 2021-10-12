--  @testpoint:openGauss关键字position(非保留)，同时作为表名和列名带引号，并进行dml操作,position列的值最终显示为1000

drop table if exists "position";
create table "position"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"position" varchar(100) default 'position'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "position"(c_id,"position") values(1,'hello');
insert into "position"(c_id,"position") values(2,'china');
update "position" set "position"=1000 where "position"='hello';
delete from "position" where "position"='china';
select "position" from "position" where "position"!='hello' order by "position";

drop table "position";

