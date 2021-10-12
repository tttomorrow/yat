--  @testpoint:openGauss关键字prepared(非保留)，同时作为表名和列名带引号，并进行dml操作,prepared列的值最终显示为1000

drop table if exists "prepared";
create table "prepared"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"prepared" varchar(100) default 'prepared'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "prepared"(c_id,"prepared") values(1,'hello');
insert into "prepared"(c_id,"prepared") values(2,'china');
update "prepared" set "prepared"=1000 where "prepared"='hello';
delete from "prepared" where "prepared"='china';
select "prepared" from "prepared" where "prepared"!='hello' order by "prepared";

drop table "prepared";

