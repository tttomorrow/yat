--  @testpoint:openGauss关键字forward(非保留)，同时作为表名和列名带引号，并进行dml操作,forward列的值最终显示为1000

drop table if exists "forward";
create table "forward"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"forward" varchar(100) default 'forward'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "forward"(c_id,"forward") values(1,'hello');
insert into "forward"(c_id,"forward") values(2,'china');
update "forward" set "forward"=1000 where "forward"='hello';
delete from "forward" where "forward"='china';
select "forward" from "forward" where "forward"!='hello' order by "forward";

drop table "forward";

