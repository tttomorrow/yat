--  @testpoint:openGauss关键字share(非保留)，同时作为表名和列名带引号，并进行dml操作,share列的值最终显示为1000

drop table if exists "share" CASCADE;
create table "share"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"share" varchar(100) default 'share'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "share"(c_id,"share") values(1,'hello');
insert into "share"(c_id,"share") values(2,'china');
update "share" set "share"=1000 where "share"='hello';
delete from "share" where "share"='china';
select "share" from "share" where "share"!='hello' order by "share";

drop table "share";

