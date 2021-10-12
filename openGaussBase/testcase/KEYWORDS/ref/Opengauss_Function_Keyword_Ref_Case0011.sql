--  @testpoint:openGauss关键字ref(非保留)，同时作为表名和列名带引号，并进行dml操作,ref列的值最终显示为1000

drop table if exists "ref";
create table "ref"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"ref" varchar(100) default 'ref'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "ref"(c_id,"ref") values(1,'hello');
insert into "ref"(c_id,"ref") values(2,'china');
update "ref" set "ref"=1000 where "ref"='hello';
delete from "ref" where "ref"='china';
select "ref" from "ref" where "ref"!='hello' order by "ref";

drop table "ref";

