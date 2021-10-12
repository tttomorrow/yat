-- @testpoint: insert语句绑定布尔类型

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

--创建存储过程
create or replace procedure pro_001()
as
    sqlstat varchar(500);
	v1 boolean;
	v2 boolean;
	v3 boolean;
begin
    v1 := true;
    v2 := false;
    v3 := 10;
    sqlstat := 'insert into all_datatype_tbl(c_boolean) select :p1';
    execute immediate sqlstat using v1;
    execute immediate sqlstat using v2;
    execute immediate sqlstat using v3;
end;
/
--调用存储过程
call pro_001();

--查看表数据
select c_boolean from all_datatype_tbl;

--清理环境
drop procedure pro_001;
drop table all_datatype_tbl;