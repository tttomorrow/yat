--  @testpoint:openGauss关键字statistics(非保留)，同时作为表名和列名带引号，并进行dml操作,statistics列的值最终显示为1000

drop table if exists "statistics" CASCADE;
create table "statistics"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"statistics" varchar(100) default 'statistics'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "statistics"(c_id,"statistics") values(1,'hello');
insert into "statistics"(c_id,"statistics") values(2,'china');
update "statistics" set "statistics"=1000 where "statistics"='hello';
delete from "statistics" where "statistics"='china';
select "statistics" from "statistics" where "statistics"!='hello' order by "statistics";

drop table "statistics";

