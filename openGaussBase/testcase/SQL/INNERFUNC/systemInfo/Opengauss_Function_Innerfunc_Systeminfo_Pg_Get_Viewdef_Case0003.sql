-- @testpoint: 为视图获取底层的SELECT命令；行字段被换到指定的列数，打印是隐含的
drop table if exists test_view CASCADE;
create table test_view(a varchar);
insert into  test_view values('default');
CREATE VIEW myview AS SELECT * FROM test_view WHERE a = 'pg_default';
select pg_get_viewdef(oid,1) from PG_CLASS where relname='myview' ;
drop table if exists test_view CASCADE;