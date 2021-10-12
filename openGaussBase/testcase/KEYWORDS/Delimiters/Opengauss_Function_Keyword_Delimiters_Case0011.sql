--  @testpoint:openGauss关键字delimiters(非保留)，同时作为表名和列名带引号，并进行dml操作,delimiters列的值最终显示为1000

drop table if exists "delimiters";
create table "delimiters"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"delimiters" varchar(100) default 'delimiters'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "delimiters"(c_id,"delimiters") values(1,'hello');
insert into "delimiters"(c_id,"delimiters") values(2,'china');
update "delimiters" set "delimiters"=1000 where "delimiters"='hello';
delete from "delimiters" where "delimiters"='china';
select "delimiters" from "delimiters" where "delimiters"!='hello' order by "delimiters";

drop table "delimiters";

