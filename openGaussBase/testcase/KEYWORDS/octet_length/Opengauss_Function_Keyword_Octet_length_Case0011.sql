--  @testpoint:openGauss关键字octet_length(非保留)，同时作为表名和列名带引号，并进行dml操作,octet_length列的值最终显示为1000

drop table if exists "octet_length";
create table "octet_length"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"octet_length" varchar(100) default 'octet_length'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "octet_length"(c_id,"octet_length") values(1,'hello');
insert into "octet_length"(c_id,"octet_length") values(2,'china');
update "octet_length" set "octet_length"=1000 where "octet_length"='hello';
delete from "octet_length" where "octet_length"='china';
select "octet_length" from "octet_length" where "octet_length"!='hello' order by "octet_length";

drop table "octet_length";

