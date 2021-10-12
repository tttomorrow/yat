--  @testpoint:openGauss保留关键字session_user同时作为表名和列名带引号，并进行dml操作,session_user列的值最终显示为1000
drop table if exists "session_user";
create table "session_user"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"session_user" varchar(100) default 'session_user'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--插入数据
insert into "session_user"(c_id,"session_user") values(1,'hello');
insert into "session_user"(c_id,"session_user") values(2,'china');

--更新表数据
update "session_user" set "session_user"=1000 where "session_user"='hello';

--清理表数据
delete from "session_user" where "session_user"='china';

--查看表数据
select "session_user" from "session_user" where "session_user"!='hello' order by "session_user";

--清理环境
drop table "session_user";