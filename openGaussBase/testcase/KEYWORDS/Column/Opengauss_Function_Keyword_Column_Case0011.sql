--  @testpoint:openGauss保留关键字column同时作为表名和列名带引号，并进行dml操作,column列的值最终显示为1000
drop table if exists "column";
create table "column"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"column" varchar(100) default 'column'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "column"(c_id,"column") values(1,'hello');
insert into "column"(c_id,"column") values(2,'china');
update "column" set "column"=1000 where "column"='hello';
delete from "column" where "column"='china';
select "column" from "column" where "column"!='hello' order by "column";

drop table "column";