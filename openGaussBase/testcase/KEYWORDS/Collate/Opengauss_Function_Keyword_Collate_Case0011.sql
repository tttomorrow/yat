--  @testpoint:openGauss保留关键字collate同时作为表名和列名带引号，并进行dml操作,collate列的值最终显示为1000
drop table if exists "collate";
create table "collate"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"collate" varchar(100) default 'collate'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "collate"(c_id,"collate") values(1,'hello');
insert into "collate"(c_id,"collate") values(2,'china');
update "collate" set "collate"=1000 where "collate"='hello';
delete from "collate" where "collate"='china';
select "collate" from "collate" where "collate"!='hello' order by "collate";

drop table "collate";