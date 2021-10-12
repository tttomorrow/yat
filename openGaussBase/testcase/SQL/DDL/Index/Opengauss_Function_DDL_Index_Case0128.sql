--  @testpoint:reset：FILLFACTOR:0-100

--建表
DROP TABLE if EXISTS test_index_table_128 CASCADE;
create table test_index_table_128(
c_int int,
c_date date
) WITH (ORIENTATION = row) partition by range(c_date)(
partition p1 values less than ('1990-01-01 00:00:00')
);

--建索引
drop index if exists index_128_01;
create index index_128_01 on test_index_table_128(c_date) with (fillfactor=50);
select relname from pg_class where relname like 'index_128_%' order by relname;

--reset
ALTER index index_128_01 set (FILLFACTOR=10);
ALTER index index_128_01 reset (FILLFACTOR);
--清理环境
DROP TABLE if EXISTS test_index_table_128 CASCADE;