--  @testpoint:openGauss关键字Large(非保留)，同时作为表名和列名带引号，并进行dml操作,Large列的值最终显示为1000

drop table if exists "Large";
create table "Large"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Large" varchar(100) default 'Large'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "Large"(c_id,"Large") values(1,'hello');
insert into "Large"(c_id,"Large") values(2,'china');
update "Large" set "Large"=1000 where "Large"='hello';
delete from "Large" where "Large"='china';
select "Large" from "Large" where "Large"!='hello' order by "Large";

drop table "Large";

