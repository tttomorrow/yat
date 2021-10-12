--  @testpoint:openGauss关键字sequences(非保留)，同时作为表名和列名带引号，并进行dml操作,sequences列的值最终显示为1000

drop table if exists "sequences" CASCADE;
create table "sequences"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"sequences" varchar(100) default 'sequences'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "sequences"(c_id,"sequences") values(1,'hello');
insert into "sequences"(c_id,"sequences") values(2,'china');
update "sequences" set "sequences"=1000 where "sequences"='hello';
delete from "sequences" where "sequences"='china';
select "sequences" from "sequences" where "sequences"!='hello' order by "sequences";

drop table "sequences";

