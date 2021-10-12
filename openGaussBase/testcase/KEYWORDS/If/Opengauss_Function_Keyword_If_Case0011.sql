--  @testpoint:openGauss关键字If(非保留)，同时作为表名和列名带引号，并进行dml操作,If列的值最终显示为1000

drop table if exists "If";
create table "If"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"If" varchar(100) default 'If'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "If"(c_id,"If") values(1,'hello');
insert into "If"(c_id,"If") values(2,'china');
update "If" set "If"=1000 where "If"='hello';
delete from "If" where "If"='china';
select "If" from "If" where "If"!='hello' order by "If";

drop table "If";
