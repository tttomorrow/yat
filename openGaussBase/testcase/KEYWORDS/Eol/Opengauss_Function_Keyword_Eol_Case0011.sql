--  @testpoint:openGauss关键字eol(非保留)，同时作为表名和列名带引号，并进行dml操作,eol列的值最终显示为1000

drop table if exists "eol";
create table "eol"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"eol" varchar(100) default 'eol'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "eol"(c_id,"eol") values(1,'hello');
insert into "eol"(c_id,"eol") values(2,'china');
update "eol" set "eol"=1000 where "eol"='hello';
delete from "eol" where "eol"='china';
select "eol" from "eol" where "eol"!='hello' order by "eol";

drop table "eol";

