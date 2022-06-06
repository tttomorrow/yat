--  @testpoint:openGauss关键字store(非保留)，同时作为表名和列名带引号，并进行dml操作,store列的值最终显示为1000

drop table if exists "store" CASCADE;
create table "store"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"store" varchar(100) default 'store'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "store"(c_id,"store") values(1,'hello');
insert into "store"(c_id,"store") values(2,'china');
update "store" set "store"=1000 where "store"='hello';
delete from "store" where "store"='china';
select "store" from "store" where "store"!='hello' order by "store";

drop table "store";

