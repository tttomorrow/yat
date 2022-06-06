--  @testpoint:openGauss关键字Implicit(非保留)，同时作为表名和列名带引号，并进行dml操作,Implicit列的值最终显示为1000

drop table if exists "Implicit";
create table "Implicit"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Implicit" varchar(100) default 'Implicit'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "Implicit"(c_id,"Implicit") values(1,'hello');
insert into "Implicit"(c_id,"Implicit") values(2,'china');
update "Implicit" set "Implicit"=1000 where "Implicit"='hello';
delete from "Implicit" where "Implicit"='china';
select "Implicit" from "Implicit" where "Implicit"!='hello' order by "Implicit";

drop table "Implicit";

