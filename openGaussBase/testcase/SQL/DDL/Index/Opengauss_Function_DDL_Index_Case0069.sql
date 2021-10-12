--  @testpoint: --column_name：行存临时表常用数据类型32列：successs
DROP TABLE if EXISTS test_index_table_069 CASCADE;
create temporary table test_index_table_069(
c_int1 INTEGER,
c_int2 INTEGER,
c_int3 INTEGER,
c_int4 INTEGER,
c_int5 INTEGER,
c_int6 INTEGER,
c_int7 INTEGER,
c_int8 INTEGER,
c_int9 INTEGER,
c_int10 INTEGER,
c_int11 INTEGER,
c_int12 INTEGER,
c_int13 INTEGER,
c_int14 INTEGER,
c_int15 INTEGER,
c_int16 INTEGER,
c_int17 INTEGER,
c_int18 INTEGER,
c_int19 INTEGER,
c_int20 INTEGER,
c_int21 INTEGER,
c_int22 INTEGER,
c_int23 INTEGER,
c_int24 INTEGER,
c_int25 INTEGER,
c_int26 INTEGER,
c_int27 INTEGER,
c_int28 INTEGER,
c_int29 INTEGER,
c_int30 INTEGER,
c_int31 INTEGER,
c_int32 INTEGER

) WITH (ORIENTATION = row);

--建psort索引
drop index if exists index_069_01;

create index index_069_01 on test_index_table_069(c_int1,
c_int2,
c_int3,
c_int4,
c_int5,
c_int6,
c_int7,
c_int8,
c_int9,
c_int10,
c_int11,
c_int12,
c_int13,
c_int14,
c_int15,
c_int16,
c_int17,
c_int18,
c_int19,
c_int20,
c_int21,
c_int22,
c_int23,
c_int24,
c_int25,
c_int26,
c_int27,
c_int28,
c_int29,
c_int30,
c_int31,
c_int32);

select relname from pg_class where relname like 'index_069_%' order by relname;

--btree
drop index if exists index_069_01;


create index index_069_01 on test_index_table_069 using btree(c_int1,
c_int2,
c_int3,
c_int4,
c_int5,
c_int6,
c_int7,
c_int8,
c_int9,
c_int10,
c_int11,
c_int12,
c_int13,
c_int14,
c_int15,
c_int16,
c_int17,
c_int18,
c_int19,
c_int20,
c_int21,
c_int22,
c_int23,
c_int24,
c_int25,
c_int26,
c_int27,
c_int28,
c_int29,
c_int30,
c_int31,
c_int32);

select relname from pg_class where relname like 'index_069_%' order by relname;

--gin
drop index if exists index_069_01;
drop index if exists index_069_02;
drop index if exists index_069_03;
drop index if exists index_069_04;
drop index if exists index_069_05;
drop index if exists index_069_06;
drop index if exists index_069_07;
drop index if exists index_069_08;
drop index if exists index_069_09;
drop index if exists index_069_10;

create index index_069_01 on test_index_table_069 using gin(to_tsvector('english', c_int1),
to_tsvector('english', c_int2),
to_tsvector('english', c_int3),
to_tsvector('english', c_int4),
to_tsvector('english', c_int5),
to_tsvector('english', c_int6),
to_tsvector('english', c_int7),
to_tsvector('english', c_int8),
to_tsvector('english', c_int9),
to_tsvector('english', c_int10),
to_tsvector('english', c_int11),
to_tsvector('english', c_int12),
to_tsvector('english', c_int13),
to_tsvector('english', c_int14),
to_tsvector('english', c_int15),
to_tsvector('english', c_int16),
to_tsvector('english', c_int17),
to_tsvector('english', c_int18),
to_tsvector('english', c_int19),
to_tsvector('english', c_int20),
to_tsvector('english', c_int21),
to_tsvector('english', c_int22),
to_tsvector('english', c_int23),
to_tsvector('english', c_int24),
to_tsvector('english', c_int25),
to_tsvector('english', c_int26),
to_tsvector('english', c_int27),
to_tsvector('english', c_int28),
to_tsvector('english', c_int29),
to_tsvector('english', c_int30),
to_tsvector('english', c_int31),
to_tsvector('english', c_int32));

select relname from pg_class where relname like 'index_069_%' order by relname;

--清理环境
DROP TABLE if EXISTS test_index_table_069 CASCADE;