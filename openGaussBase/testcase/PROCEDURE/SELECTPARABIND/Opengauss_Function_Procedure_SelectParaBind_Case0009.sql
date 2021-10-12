-- @testpoint: 使用重复的占位符

--创建测试表
drop table if exists all_datatype_tbl;
create table all_datatype_tbl(
	c_id integer,
	c_boolean boolean,
	c_integer integer, c_bigint bigint,
	c_real real,
	c_decimal decimal(38), c_number number(38),
	c_char char(50) default null, c_varchar varchar(50), c_clob clob,
    c_blob blob,
	 c_timestamp timestamp, c_interval interval day to second);

--创建匿名块
declare
    sqlstat varchar(500);
	v1 char(10);
	v2 char(10);
begin
    v1 := 'abc';
    v2 := 'efg';
    sqlstat := null;
    execute immediate 'insert into all_datatype_tbl(c_char,c_varchar) values(:p1,:p1)' using v1,v2;
end;
/
--查看表数据
select c_char,c_varchar from all_datatype_tbl;

--清理环境
drop table all_datatype_tbl;