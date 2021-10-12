--  @testpoint:openGauss关键字nocompress(非保留)，同时作为表名和列名带引号，并进行dml操作,nocompress列的值最终显示为1000

drop table if exists "nocompress";
create table "nocompress"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"nocompress" varchar(100) default 'nocompress'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "nocompress"(c_id,"nocompress") values(1,'hello');
insert into "nocompress"(c_id,"nocompress") values(2,'china');
update "nocompress" set "nocompress"=1000 where "nocompress"='hello';
delete from "nocompress" where "nocompress"='china';
select "nocompress" from "nocompress" where "nocompress"!='hello' order by "nocompress";

drop table "nocompress";

