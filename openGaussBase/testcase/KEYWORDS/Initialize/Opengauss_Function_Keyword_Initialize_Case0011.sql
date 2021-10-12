--  @testpoint:openGauss关键字Initialize(非保留)，同时作为表名和列名带引号，并进行dml操作,Initialize列的值最终显示为1000

drop table if exists "Initialize";
create table "Initialize"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Initialize" varchar(100) default 'Initialize'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "Initialize"(c_id,"Initialize") values(1,'hello');
insert into "Initialize"(c_id,"Initialize") values(2,'china');
update "Initialize" set "Initialize"=1000 where "Initialize"='hello';
delete from "Initialize" where "Initialize"='china';
select "Initialize" from "Initialize" where "Initialize"!='hello' order by "Initialize";

drop table "Initialize";

