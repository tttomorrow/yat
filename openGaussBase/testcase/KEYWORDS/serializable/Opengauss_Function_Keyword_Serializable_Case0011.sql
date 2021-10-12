--  @testpoint:openGauss关键字serializable(非保留)，同时作为表名和列名带引号，并进行dml操作,serializable列的值最终显示为1000

drop table if exists "serializable" CASCADE;
create table "serializable"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"serializable" varchar(100) default 'serializable'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "serializable"(c_id,"serializable") values(1,'hello');
insert into "serializable"(c_id,"serializable") values(2,'china');
update "serializable" set "serializable"=1000 where "serializable"='hello';
delete from "serializable" where "serializable"='china';
select "serializable" from "serializable" where "serializable"!='hello' order by "serializable";

drop table "serializable";

