--  @testpoint:openGauss关键字move(非保留)，同时作为表名和列名带引号，并进行dml操作,move列的值最终显示为1000

drop table if exists "move";
create table "move"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"move" varchar(100) default 'move'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "move"(c_id,"move") values(1,'hello');
insert into "move"(c_id,"move") values(2,'china');
update "move" set "move"=1000 where "move"='hello';
delete from "move" where "move"='china';
select "move" from "move" where "move"!='hello' order by "move";

drop table "move";
