--  @testpoint: set：FILLFACTOR:10-100

--建表
DROP TABLE if EXISTS test_index_table_123 CASCADE;
create table test_index_table_123(
c_int int,
c_date date
) WITH (ORIENTATION = row) partition by range(c_date)(
partition p1 values less than ('1990-01-01 00:00:00')
);

--建索引
drop index if exists index_123_01;
create index index_123_01 on test_index_table_123(c_date) with (fillfactor=50);
select relname from pg_class where relname like 'index_123_%' order by relname;

--set
ALTER index index_123_01 SET (FILLFACTOR=10);
ALTER index index_123_01 SET (FILLFACTOR=50);
ALTER index index_123_01 SET (FILLFACTOR=100);

--清理环境
DROP TABLE if EXISTS test_index_table_123 CASCADE;