-- @testpoint: clob：行存分区表clob修改修改为其他类型再改回clob：可拓展为各数据类型：success


--删表
drop table if exists test_clob_34 cascade;
create table test_clob_34(id int,
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
) WITH (ORIENTATION = row)
PARTITION BY RANGE(id)(
        PARTITION P1 VALUES LESS THAN(100),
        PARTITION P2 VALUES LESS THAN(1000),
        PARTITION P3 VALUES LESS THAN(MAXVALUE))
;
--修改为其他数据类型
alter table test_clob_34 modify (
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
where c.relname = 'test_clob_34' and a.attrelid = c.oid and a.attnum>0 order by a.attname asc;

--修改为clob
alter table test_clob_34 modify (
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
where c.relname = 'test_clob_34' and a.attrelid = c.oid and a.attnum>0 order by a.attname asc;
--清理数据
drop table if exists test_clob_34 CASCADE;