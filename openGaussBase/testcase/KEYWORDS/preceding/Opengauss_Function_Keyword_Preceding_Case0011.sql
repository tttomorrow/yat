--  @testpoint:openGauss关键字preceding(非保留)，同时作为表名和列名带引号，并进行dml操作,preceding列的值最终显示为1000

drop table if exists "preceding";
create table "preceding"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"preceding" varchar(100) default 'preceding'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "preceding"(c_id,"preceding") values(1,'hello');
insert into "preceding"(c_id,"preceding") values(2,'china');
update "preceding" set "preceding"=1000 where "preceding"='hello';
delete from "preceding" where "preceding"='china';
select "preceding" from "preceding" where "preceding"!='hello' order by "preceding";

drop table "preceding";

