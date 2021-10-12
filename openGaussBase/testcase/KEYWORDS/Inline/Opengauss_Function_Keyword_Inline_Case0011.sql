--  @testpoint:openGauss关键字Inline(非保留)，同时作为表名和列名带引号，并进行dml操作,Inline列的值最终显示为1000

drop table if exists "Inline";
create table "Inline"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Inline" varchar(100) default 'Inline'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "Inline"(c_id,"Inline") values(1,'hello');
insert into "Inline"(c_id,"Inline") values(2,'china');
update "Inline" set "Inline"=1000 where "Inline"='hello';
delete from "Inline" where "Inline"='china';
select "Inline" from "Inline" where "Inline"!='hello' order by "Inline";

drop table "Inline";

