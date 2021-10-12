--  @testpoint:openGauss关键字maxtrans(非保留)，同时作为表名和列名带引号，并进行dml操作,maxtrans列的值最终显示为1000

drop table if exists "maxtrans";
create table "maxtrans"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"maxtrans" varchar(100) default 'maxtrans'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "maxtrans"(c_id,"maxtrans") values(1,'hello');
insert into "maxtrans"(c_id,"maxtrans") values(2,'china');
update "maxtrans" set "maxtrans"=1000 where "maxtrans"='hello';
delete from "maxtrans" where "maxtrans"='china';
select "maxtrans" from "maxtrans" where "maxtrans"!='hello' order by "maxtrans";

drop table "maxtrans";

