-- @testpoint: 为视图获取底层的SELECT命令(oid获取)
drop table if exists test_view CASCADE;
create table test_view(a varchar);
insert into  test_view values('default');
CREATE VIEW myview AS SELECT * FROM test_view WHERE a = 'pg_default';
select pg_get_viewdef(oid) from PG_CLASS where relname='myview' ;
drop table if exists test_view CASCADE;