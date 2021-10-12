--  @testpoint:UNUSABLE：列存表设置索引不可用：不支持

--建普通表
DROP TABLE if EXISTS test_index_table_130 CASCADE;
create table test_index_table_130(
c_int int
) WITH (ORIENTATION = column) ;

begin
    for i in 0..10000 loop
        insert into test_index_table_130 values(i);
    end loop;
end;
/

--建索引
drop index if exists index_130_01;
create index index_130_01 on test_index_table_130(c_int) ;
select relname from pg_class where relname like 'index_130_%' order by relname;


ALTER INDEX  index_130_02 UNUSABLE;
ALTER INDEX  IF EXISTS  index_130_02 UNUSABLE;
--Un-support feature
ALTER INDEX  IF EXISTS  index_130_01 UNUSABLE;


--建临时表
DROP TABLE if EXISTS test_index_table_130 CASCADE;
create temporary table test_index_table_130(
c_int int
) WITH (ORIENTATION = column) ;

begin
    for i in 0..10000 loop
        insert into test_index_table_130 values(i);
    end loop;
end;
/

--建索引
drop index if exists index_130_01;
create index index_130_01 on test_index_table_130(c_int) ;
select relname from pg_class where relname like 'index_130_%' order by relname;


ALTER INDEX  index_130_02 UNUSABLE;
ALTER INDEX  IF EXISTS  index_130_02 UNUSABLE;
--Un-support feature
ALTER INDEX  IF EXISTS  index_130_01 UNUSABLE;


--清理环境
DROP TABLE if EXISTS test_index_table_130 CASCADE;