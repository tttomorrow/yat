-- @testpoint: clob：行存普通表clob修改修改为其他类型再改回clob：可拓展为各数据类型：success
--建表
drop table if exists test_clob_36 CASCADE;
create table test_clob_36(
name1 CLOB,
name2 CLOB,
name3 CLOB,
name4 CLOB,
name5 CLOB,
name6 CLOB,
name7 CLOB,
name8 CLOB,
name9 CLOB,
name10 CLOB,
name11 CLOB,
name12 CLOB,
name13 CLOB,
name14 CLOB,
name15 CLOB,
name16 CLOB,
name17 CLOB,
name18 CLOB,
name19 CLOB,
name20 CLOB,
name21 CLOB,
name22 CLOB,
name23 CLOB
) with (orientation=row);
--插入数据
--查询字段信息
SELECT a.attname,format_type(a.atttypid,a.atttypmod) as type
FROM pg_class as c,pg_attribute as a
where c.relname = 'test_clob_36' and a.attrelid = c.oid and a.attnum>0 order by a.attname asc;
--clob修改为其他类型
alter table test_clob_36 modify (
name1 INTEGER,
name2 BIGINT,
name3 NUMERIC,
name4 NUMBER,
name5 CHAR,
name8 REAL,
name9 DOUBLE PRECISION,
name10 FLOAT,
name11 BINARY_DOUBLE,
name12 DEC,
name13 NCHAR,
name14 VARCHAR,
name15 CLOB,
name16 TEXT,
name20 DATE
);
--查询字段信息
SELECT a.attname,format_type(a.atttypid,a.atttypmod) as type
FROM pg_class as c,pg_attribute as a
where c.relname = 'test_clob_36' and a.attrelid = c.oid and a.attnum>0 order by a.attname asc;

--修改回clob
alter table test_clob_36 modify (
name1 CLOB,
name2 CLOB,
name3 CLOB,
name4 CLOB,
name5 CLOB,
name6 CLOB,
name7 CLOB,
name8 CLOB,
name9 CLOB,
name10 CLOB,
name11 CLOB,
name12 CLOB,
name13 CLOB,
name14 CLOB,
name15 CLOB,
name16 CLOB,
name17 CLOB,
name18 CLOB,
name19 CLOB,
name20 CLOB,
name21 CLOB,
name22 CLOB,
name23 CLOB
);
--查询字段信息
SELECT a.attname,format_type(a.atttypid,a.atttypmod) as type
FROM pg_class as c,pg_attribute as a
where c.relname = 'test_clob_36' and a.attrelid = c.oid and a.attnum>0 order by a.attname asc;

--清理数据
drop table if exists test_clob_36 CASCADE;