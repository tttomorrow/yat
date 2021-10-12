--  @testpoint: clob：列存普通表其他类型修改为clob：可拓展为各数据类型
drop table if exists test_clob_10 CASCADE;
create table test_clob_10(
name1 INTEGER,
name2 BIGINT,
name3 NUMERIC,
name4 NUMBER,
name5 CHAR,
name6 BOOLEAN,
name7 money,
name8 REAL,
name9 DOUBLE PRECISION,
name10 FLOAT,
name11 BINARY_DOUBLE,
name12 DEC,
name13 NCHAR,
name14 VARCHAR,
name15 CLOB,
name16 TEXT,
name19 BYTEA,
name20 DATE,
name22 cidr

) with (orientation=column);
--插入数据
--查询字段信息
SELECT format_type(a.atttypid,a.atttypmod) as type
FROM pg_class as c,pg_attribute as a
where c.relname = 'test_clob_10' and a.attrelid = c.oid and a.attnum>0;
--修改数据类型为clob
alter table test_clob_10 modify (name1 CLOB,
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
name19 CLOB,
name20 CLOB,
name22 CLOB);
--查询字段信息
SELECT format_type(a.atttypid,a.atttypmod) as type
FROM pg_class as c,pg_attribute as a
where c.relname = 'test_clob_10' and a.attrelid = c.oid and a.attnum>0;
--清理数据
drop table if exists test_clob_10 CASCADE;