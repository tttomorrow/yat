--  @testpoint:openGauss关键字Handler(非保留)，同时作为表名和列名带引号，并进行dml操作,Handler列的值最终显示为1000

drop table if exists "Handler";
create table "Handler"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Handler" varchar(100) default 'Handler'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "Handler"(c_id,"Handler") values(1,'hello');
insert into "Handler"(c_id,"Handler") values(2,'china');
update "Handler" set "Handler"=1000 where "Handler"='hello';
delete from "Handler" where "Handler"='china';
select "Handler" from "Handler" where "Handler"!='hello' order by "Handler";

drop table "Handler";
