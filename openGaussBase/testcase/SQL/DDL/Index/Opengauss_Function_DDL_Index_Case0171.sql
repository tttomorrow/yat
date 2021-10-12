--  @testpoint: 在同一列建索引1000+次

--建普通表
DROP TABLE if EXISTS test_index_table_171 CASCADE;
create table test_index_table_171(
c_int int
) WITH (ORIENTATION = row) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);

declare
sqlstat varchar;
name varchar;
begin
    for i in 0..1000 loop

        name := 'index_171_'||i||'';
        sqlstat := 'drop index if exists '||name||';';
        execute immediate sqlstat;
        sqlstat := 'create index '||name||' on test_index_table_171 using btree(c_int);';
        execute immediate sqlstat;

    end loop;
end;
/

select count(relname) from pg_class where relname like 'index_171_%';
explain select c_int from test_index_table_171 where c_int > 5000 group by c_int;

--清理环境
DROP TABLE if EXISTS test_index_table_171 CASCADE;
