-- @testpoint: column_name：行存普通表各数据类型1列：合理报错
DROP TABLE if EXISTS test_index_table_056 CASCADE;
create table test_index_table_056(name1 TINYINT,name2 BIGINT,
name3 NUMERIC,name4 SMALLSERIAL,name5 SERIAL,name6 BIGSERIAL,name7 FLOAT,
name8 BINARY_DOUBLE,name9 DEC,name10 BOOLEAN,name12 CHAR,name13 CLOB,
name14 TEXT,name15 BLOB,name16 RAW,name17 BYTEA,name18 DATE,name19 INTERVAL,
name20 reltime,name21 cidr,name22 bit,name23 tsvector,name24 tsquery
);
--建索引 btree
drop index if exists index_056_01,index_056_02,index_056_03,index_056_04,index_056_05;
drop index if exists index_056_06,index_056_07,index_056_08,index_056_09,index_056_10;
drop index if exists index_056_12,index_056_13,index_056_14,index_056_15;
drop index if exists index_056_16,index_056_17,index_056_18,index_056_19,index_056_20;
drop index if exists index_056_21,index_056_22,index_056_23,index_056_24;
create index index_056_01 on test_index_table_056(name1);
create index index_056_02 on test_index_table_056(name2);
create index index_056_03 on test_index_table_056(name3);
create index index_056_04 on test_index_table_056(name4);
create index index_056_05 on test_index_table_056(name5);
create index index_056_06 on test_index_table_056(name6);
create index index_056_07 on test_index_table_056(name7);
create index index_056_08 on test_index_table_056(name8);
create index index_056_09 on test_index_table_056(name9);
create index index_056_10 on test_index_table_056(name10);
create index index_056_12 on test_index_table_056(name12);
create index index_056_13 on test_index_table_056(name13);
create index index_056_14 on test_index_table_056(name14);
create index index_056_15 on test_index_table_056(name15);
create index index_056_16 on test_index_table_056(name16);
create index index_056_17 on test_index_table_056(name17);
create index index_056_18 on test_index_table_056(name18);
create index index_056_19 on test_index_table_056(name19);
create index index_056_20 on test_index_table_056(name20);
create index index_056_21 on test_index_table_056(name21);
create index index_056_22 on test_index_table_056(name22);
create index index_056_23 on test_index_table_056(name23);
create index index_056_24 on test_index_table_056(name24);

--查询索引
select relname from pg_class where relname like 'index_056%' order by relname asc;


--创建gin索引
drop index if exists index_056_01,index_056_02,index_056_03,index_056_04,index_056_05;
drop index if exists index_056_06,index_056_07,index_056_08,index_056_09,index_056_10;
drop index if exists index_056_11,index_056_12,index_056_13,index_056_14,index_056_15;
drop index if exists index_056_16,index_056_17,index_056_18,index_056_19,index_056_20;
drop index if exists index_056_21,index_056_22,index_056_23,index_056_24;

create index index_056_01 on test_index_table_056 using gin(to_tsvector('english', name1));
create index index_056_02 on test_index_table_056 using gin(to_tsvector('english', name2));
create index index_056_03 on test_index_table_056 using gin(to_tsvector('english', name3));
create index index_056_04 on test_index_table_056 using gin(to_tsvector('english', name4));
create index index_056_05 on test_index_table_056 using gin(to_tsvector('english', name5));
create index index_056_06 on test_index_table_056 using gin(to_tsvector('english', name6));
create index index_056_07 on test_index_table_056 using gin(to_tsvector('english', name7));
create index index_056_08 on test_index_table_056 using gin(to_tsvector('english', name8));
create index index_056_09 on test_index_table_056 using gin(to_tsvector('english', name9));
create index index_056_10 on test_index_table_056 using gin(to_tsvector('english', name10));
create index index_056_12 on test_index_table_056 using gin(to_tsvector('english', name12));
create index index_056_13 on test_index_table_056 using gin(to_tsvector('english', name13));
create index index_056_14 on test_index_table_056 using gin(to_tsvector('english', name14));
create index index_056_15 on test_index_table_056 using gin(to_tsvector('english', name15));
create index index_056_16 on test_index_table_056 using gin(to_tsvector('english', name16));
create index index_056_17 on test_index_table_056 using gin(to_tsvector('english', name17));
create index index_056_18 on test_index_table_056 using gin(to_tsvector('english', name18));
create index index_056_19 on test_index_table_056 using gin(to_tsvector('english', name19));
create index index_056_20 on test_index_table_056 using gin(to_tsvector('english', name20));
create index index_056_21 on test_index_table_056 using gin(to_tsvector('english', name21));
create index index_056_22 on test_index_table_056 using gin(to_tsvector('english', name22));
create index index_056_23 on test_index_table_056 using gin(to_tsvector('english', name23));
create index index_056_24 on test_index_table_056 using gin(to_tsvector('english', name24));

--查询索引
select relname from pg_class where relname like 'index_056_%' order by relname asc;

--清理数据
DROP TABLE if EXISTS test_index_table_056 CASCADE;
