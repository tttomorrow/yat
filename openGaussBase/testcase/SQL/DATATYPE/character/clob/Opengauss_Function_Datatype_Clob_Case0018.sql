--  @testpoint: clob：to_clob：各数据类型转换为clob：success：实际资料有问题：nvarchar
--建表
drop table if exists test_clob_18 CASCADE;
create table test_clob_18(id int,name clob);
--raw
insert into test_clob_18 VALUES(1, to_clob(hextoraw('7D')));
--char
insert into test_clob_18 VALUES(2, to_clob(cast('t' as char)));
--nchar
insert into test_clob_18 VALUES(3, to_clob(cast('test_clob' as nchar)));
--varchar
insert into test_clob_18 VALUES(4, to_clob(cast('test_clob' as varchar)));
--nvarchar
--insert into test_clob_18 VALUES(5, to_clob(cast('test_clob' as nvarchar)));
--varchar2
insert into test_clob_18 VALUES(6, to_clob(cast('test_clob' as varchar2)));
--NVARCHAR2
insert into test_clob_18 VALUES(7, to_clob(cast('test_clob' as NVARCHAR2)));
--text
insert into test_clob_18 VALUES(8, to_clob(cast('test_clob' as text)));

--查询字段信息
SELECT format_type(a.atttypid,a.atttypmod) as type
FROM pg_class as c,pg_attribute as a
where c.relname = 'test_clob_18' and a.attrelid = c.oid and a.attnum>0;

--清理数据
drop table if exists test_clob_18 CASCADE;