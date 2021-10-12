--  @testpoint:openGauss关键字text(非保留)，同时作为表名和列名带引号，并进行dml操作,text列的值最终显示为1000

drop table if exists "text" CASCADE;
create table "text"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"text" varchar(100) default 'text'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "text"(c_id,"text") values(1,'hello');
insert into "text"(c_id,"text") values(2,'china');
update "text" set "text"=1000 where "text"='hello';
delete from "text" where "text"='china';
select "text" from "text" where "text"!='hello' order by "text";

drop table "text";

