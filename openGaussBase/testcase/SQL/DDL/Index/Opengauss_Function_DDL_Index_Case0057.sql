--  @testpoint: column_name：行存普通表各数据类型1列：successs
DROP TABLE if EXISTS test_index_table_057 CASCADE;
create temporary table test_index_table_057(
name1 TINYINT,
name2 BIGINT,
name3 NUMERIC,
name7 FLOAT,
name8 BINARY_DOUBLE,
name9 DEC,
name10 BOOLEAN,
name12 CHAR,
name13 CLOB,
name14 TEXT,
name15 BLOB,
name16 RAW,
name17 BYTEA,
name18 DATE,
name19 INTERVAL,
name20 reltime,
name21 cidr,
name22 bit,
name23 tsvector,
name24 tsquery
);
--建索引 btree
drop index if exists index_057_01,index_057_02,index_057_03,index_057_07,index_057_08,index_057_09,index_057_10;
drop index if exists index_057_12,index_057_13,index_057_14,index_057_15;
drop index if exists index_057_16,index_057_17,index_057_18,index_057_19,index_057_20;
drop index if exists index_057_21,index_057_22,index_057_23,index_057_24;

create index index_057_01 on test_index_table_057(name1);
create index index_057_02 on test_index_table_057(name2);
create index index_057_03 on test_index_table_057(name3);
create index index_057_07 on test_index_table_057(name7);
create index index_057_08 on test_index_table_057(name8);
create index index_057_09 on test_index_table_057(name9);
create index index_057_10 on test_index_table_057(name10);
create index index_057_12 on test_index_table_057(name12);
create index index_057_13 on test_index_table_057(name13);
create index index_057_14 on test_index_table_057(name14);
create index index_057_15 on test_index_table_057(name15);
create index index_057_16 on test_index_table_057(name16);
create index index_057_17 on test_index_table_057(name17);
create index index_057_18 on test_index_table_057(name18);
create index index_057_19 on test_index_table_057(name19);
create index index_057_20 on test_index_table_057(name20);
create index index_057_21 on test_index_table_057(name21);
create index index_057_22 on test_index_table_057(name22);
create index index_057_23 on test_index_table_057(name23);
create index index_057_24 on test_index_table_057(name24);

--查询索引
select relname from pg_class where relname like 'index_057%' order by relname asc;


--创建gin索引
drop index if exists index_057_01,index_057_02,index_057_03,index_057_07,index_057_08,index_057_09,index_057_10;
drop index if exists index_057_11,index_057_12,index_057_13,index_057_14,index_057_15;
drop index if exists index_057_16,index_057_17,index_057_18,index_057_19,index_057_20;
drop index if exists index_057_21,index_057_22,index_057_23,index_057_24;

create index index_057_01 on test_index_table_057 using gin(to_tsvector('english', name1));
create index index_057_02 on test_index_table_057 using gin(to_tsvector('english', name2));
create index index_057_03 on test_index_table_057 using gin(to_tsvector('english', name3));
create index index_057_07 on test_index_table_057 using gin(to_tsvector('english', name7));
create index index_057_08 on test_index_table_057 using gin(to_tsvector('english', name8));
create index index_057_09 on test_index_table_057 using gin(to_tsvector('english', name9));
create index index_057_10 on test_index_table_057 using gin(to_tsvector('english', name10));
create index index_057_12 on test_index_table_057 using gin(to_tsvector('english', name12));
create index index_057_13 on test_index_table_057 using gin(to_tsvector('english', name13));
create index index_057_14 on test_index_table_057 using gin(to_tsvector('english', name14));
create index index_057_15 on test_index_table_057 using gin(to_tsvector('english', name15));
create index index_057_16 on test_index_table_057 using gin(to_tsvector('english', name16));
create index index_057_17 on test_index_table_057 using gin(to_tsvector('english', name17));
create index index_057_18 on test_index_table_057 using gin(to_tsvector('english', name18));
create index index_057_19 on test_index_table_057 using gin(to_tsvector('english', name19));
create index index_057_20 on test_index_table_057 using gin(to_tsvector('english', name20));
create index index_057_21 on test_index_table_057 using gin(to_tsvector('english', name21));
create index index_057_22 on test_index_table_057 using gin(to_tsvector('english', name22));
create index index_057_23 on test_index_table_057 using gin(to_tsvector('english', name23));
create index index_057_24 on test_index_table_057 using gin(to_tsvector('english', name24));

--查询索引
select relname from pg_class where relname like 'index_057_%' order by relname asc;



--清理数据
DROP TABLE if EXISTS test_index_table_057 CASCADE;
