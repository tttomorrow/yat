--  @testpoint:openGauss保留关键字fetch同时作为表名和列名带引号，并进行dml操作,fetch列的值最终显示为1000
drop table if exists "fetch";
create table "fetch"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_fetchuble real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"fetch" varchar(100) default 'fetch'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "fetch"(c_id,"fetch") values(1,'hello');
insert into "fetch"(c_id,"fetch") values(2,'china');
update "fetch" set "fetch"=1000 where "fetch"='hello';
delete from "fetch" where "fetch"='china';
select "fetch" from "fetch" where "fetch"!='hello' order by "fetch";

drop table "fetch";