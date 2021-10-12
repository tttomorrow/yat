--  @testpoint:openGauss关键字partition(非保留)，同时作为表名和列名带引号，并进行dml操作,partition列的值最终显示为1000

drop table if exists "partition";
create table "partition"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"partition" varchar(100) default 'partition'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "partition"(c_id,"partition") values(1,'hello');
insert into "partition"(c_id,"partition") values(2,'china');
update "partition" set "partition"=1000 where "partition"='hello';
delete from "partition" where "partition"='china';
select "partition" from "partition" where "partition"!='hello' order by "partition";

drop table "partition";
