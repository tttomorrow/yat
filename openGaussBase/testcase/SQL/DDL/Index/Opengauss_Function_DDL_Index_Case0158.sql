-- @testpoint:  reindex：行存设置不可用直接reindex：各索引类型+表

--建普通表
DROP TABLE if EXISTS test_index_table_158 CASCADE;
create table test_index_table_158(
c_int int
) WITH (ORIENTATION = row) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);

--建local索引
drop index if exists index_158_01;
create index index_158_01 on test_index_table_158(c_int) local (PARTITION p1,PARTITION p2,PARTITION p3,PARTITION p4);
select relname from pg_class where relname like 'index_158_%' order by relname;
explain select * from test_index_table_158 where c_int > 500 group by c_int;

--reindex
alter index index_158_01 UNUSABLE;
explain select * from test_index_table_158 where c_int > 500 group by c_int;
REINDEX INDEX  index_158_01;
explain select * from test_index_table_158 where c_int > 500 group by c_int;

--global索引
drop index if exists index_158_01;
create index index_158_01 on test_index_table_158(c_int);
--reindex
explain select * from test_index_table_158 where c_int > 500 group by c_int;
alter index index_158_01 UNUSABLE;
explain select * from test_index_table_158 where c_int > 500 group by c_int;
REINDEX INDEX  index_158_01;
explain select * from test_index_table_158 where c_int > 500 group by c_int;


--建表
DROP TABLE if EXISTS test_index_table_158 CASCADE;
create table test_index_table_158(
c_point point
) WITH (ORIENTATION = row) ;

--建gist索引
drop index if exists index_158_01;
create index index_158_01 on test_index_table_158 using gist(c_point) ;
select relname from pg_class where relname like 'index_158_%' order by relname;

--reindex
--索引可被引用
explain select * from test_index_table_158 where c_point <^ point(50,50);
ALTER INDEX  index_158_01 UNUSABLE;
explain select * from test_index_table_158 where c_point <^ point(50,50);
REINDEX INDEX  index_158_01;
explain select * from test_index_table_158 where c_point <^ point(50,50);


--建临时表
DROP TABLE if EXISTS test_index_table_158 CASCADE;
create temporary table test_index_table_158(
c_point point
) WITH (ORIENTATION = row) ;

--建gist索引
drop index if exists index_158_01;
create index index_158_01 on test_index_table_158 using gist(c_point) ;
select relname from pg_class where relname like 'index_158_%' order by relname;

--UNUSABLE
--索引可被引用
explain select * from test_index_table_158 where c_point <^ point(50,50);
ALTER INDEX  index_158_01 UNUSABLE;
explain select * from test_index_table_158 where c_point <^ point(50,50);
REINDEX INDEX  index_158_01;
explain select * from test_index_table_158 where c_point <^ point(50,50);

--清理环境
DROP TABLE if EXISTS test_index_table_158 CASCADE;