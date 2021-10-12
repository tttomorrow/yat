-- @testpoint: 统计更新带索引的表

drop table if exists analyze_005;
create table analyze_005(id int,name clob,num int);
create index INDEX_005 ON analyze_005(id,num);
insert into analyze_005 values(1,'xxxxx',2);
insert into analyze_005 values(3,'yyyyy',4);
select * from analyze_005;
analyze analyze_005((id,name));
analyze analyze_005;
select * from pg_statistic where starelid = (select oid from pg_class where relname = 'analyze_005');
alter table analyze_005 rename column id to ids;
analyze analyze_005;
select * from pg_statistic where starelid = (select oid from pg_class where relname = 'analyze_005');
alter table analyze_005 drop column ids;
analyze analyze_005;
select * from pg_statistic where starelid = (select oid from pg_class where relname = 'analyze_005');
drop table if exists analyze_005;