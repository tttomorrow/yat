--  @testpoint:openGauss关键字truncate(非保留)，同时作为表名和列名带引号，并进行dml操作,truncate列的值最终显示为1000

drop table if exists "truncate" CASCADE;
create table "truncate"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"truncate" varchar(100) default 'truncate'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "truncate"(c_id,"truncate") values(1,'hello');
insert into "truncate"(c_id,"truncate") values(2,'china');
update "truncate" set "truncate"=1000 where "truncate"='hello';
delete from "truncate" where "truncate"='china';
select "truncate" from "truncate" where "truncate"!='hello' order by "truncate";

drop table "truncate";

