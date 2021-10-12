--  @testpoint:openGauss关键字Initrans(非保留)，同时作为表名和列名带引号，并进行dml操作,Initrans列的值最终显示为1000

drop table if exists "Initrans";
create table "Initrans"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Initrans" varchar(100) default 'Initrans'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "Initrans"(c_id,"Initrans") values(1,'hello');
insert into "Initrans"(c_id,"Initrans") values(2,'china');
update "Initrans" set "Initrans"=1000 where "Initrans"='hello';
delete from "Initrans" where "Initrans"='china';
select "Initrans" from "Initrans" where "Initrans"!='hello' order by "Initrans";

drop table "Initrans";

