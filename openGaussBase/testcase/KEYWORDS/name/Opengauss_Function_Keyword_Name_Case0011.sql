--  @testpoint:openGauss关键字name(非保留)，同时作为表名和列名带引号，并进行dml操作,name列的值最终显示为1000

drop table if exists "Name";
create table "Name"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Name" varchar(100) default 'Name'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "Name"(c_id,"Name") values(1,'hello');
insert into "Name"(c_id,"Name") values(2,'china');
update "Name" set "Name"=1000 where "Name"='hello';
delete from "Name" where "Name"='china';
select "Name" from "Name" where "Name"!='hello' order by "Name";

drop table "Name";

