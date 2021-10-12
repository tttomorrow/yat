--  @testpoint:openGauss关键字nchar(非保留)，同时作为表名和列名带引号，并进行dml操作,nchar列的值最终显示为1000

drop table if exists "nchar";
create table "nchar"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"nchar" varchar(100) default 'nchar'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "nchar"(c_id,"nchar") values(1,'hello');
insert into "nchar"(c_id,"nchar") values(2,'china');
update "nchar" set "nchar"=1000 where "nchar"='hello';
delete from "nchar" where "nchar"='china';
select "nchar" from "nchar" where "nchar"!='hello' order by "nchar";

drop table "nchar";

