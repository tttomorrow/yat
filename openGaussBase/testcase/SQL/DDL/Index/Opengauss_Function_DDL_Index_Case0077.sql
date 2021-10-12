--  @testpoint: column_name：行存分区表常用数据类型31列
DROP TABLE if EXISTS test_index_table_077 CASCADE;
create table test_index_table_077(
c_float1 float,c_float2 float,c_float3 float,c_float4 float,c_float5 float,c_float6 float,c_float7 float,
c_float8 float,c_float9 float,c_float10 float,c_float11 float,c_float12 float,c_float13 float,c_float14 float,
c_float15 float,c_float16 float,c_float17 float,c_float18 float,c_float19 float,c_float20 float,c_float21 float,
c_float22 float,c_float23 float,c_float24 float,c_float25 float,c_float26 float,c_float27 float,c_float28 float,
c_float29 float,c_float30 float,c_float31 float
) WITH (ORIENTATION = row) PARTITION BY RANGE(c_float1)(PARTITION P1 VALUES LESS THAN(100));

--建psort索引：合理报错
drop index if exists index_077_01;

create index index_077_01 on test_index_table_077 using psort(c_float1,
c_float2,c_float3,c_float4,c_float5,c_float6,c_float7,c_float8,c_float9,c_float10,c_float11,c_float12,
c_float13,c_float14,c_float15,c_float16,c_float17,c_float18,c_float19,c_float20,c_float21,c_float22,
c_float23,c_float24,c_float25,c_float26,c_float27,c_float28,c_float29,c_float30,c_float31);

select relname from pg_class where relname like 'index_077_%' order by relname;

--btree：合理报错
drop index if exists index_077_01;

create index index_077_01 on test_index_table_077 using btree(c_float1,
c_float2,c_float3,c_float4,c_float5,c_float6,c_float7,c_float8,c_float9,c_float10,c_float11,c_float12,
c_float13,c_float14,c_float15,c_float16,c_float17,c_float18,c_float19,c_float20,c_float21,c_float22,
c_float23,c_float24,c_float25,c_float26,c_float27,c_float28,c_float29,c_float30,c_float31);

select relname from pg_class where relname like 'index_077_%' order by relname;

--gist：合理报错
drop index if exists index_077_01;

create index index_077_01 on test_index_table_077 using gist(c_float1,
c_float2,c_float3,c_float4,c_float5,c_float6,c_float7,c_float8,c_float9,c_float10,c_float11,c_float12,
c_float13,c_float14,c_float15,c_float16,c_float17,c_float18,c_float19,c_float20,c_float21,c_float22,
c_float23,c_float24,c_float25,c_float26,c_float27,c_float28,c_float29,c_float30,c_float31);

select relname from pg_class where relname like 'index_077_%' order by relname;

--gin：合理报错
drop index if exists index_077_01;

create index index_077_01 on test_index_table_077 using gin(to_tsvector('english', c_float1),
to_tsvector('english', c_float2),
to_tsvector('english', c_float3),
to_tsvector('english', c_float4),
to_tsvector('english', c_float5),
to_tsvector('english', c_float6),
to_tsvector('english', c_float7),
to_tsvector('english', c_float8),
to_tsvector('english', c_float9),
to_tsvector('english', c_float10),
to_tsvector('english', c_float11),
to_tsvector('english', c_float12),
to_tsvector('english', c_float13),
to_tsvector('english', c_float14),
to_tsvector('english', c_float15),
to_tsvector('english', c_float16),
to_tsvector('english', c_float17),
to_tsvector('english', c_float18),
to_tsvector('english', c_float19),
to_tsvector('english', c_float20),
to_tsvector('english', c_float21),
to_tsvector('english', c_float22),
to_tsvector('english', c_float23),
to_tsvector('english', c_float24),
to_tsvector('english', c_float25),
to_tsvector('english', c_float26),
to_tsvector('english', c_float27),
to_tsvector('english', c_float28),
to_tsvector('english', c_float29),
to_tsvector('english', c_float30),
to_tsvector('english', c_float31));

select relname from pg_class where relname like 'index_077_%' order by relname;

--清理环境
drop index if exists index_077_01;
DROP TABLE if EXISTS test_index_table_077 CASCADE;