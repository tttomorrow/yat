-- @testpoint: 收集表的统计信息后删除表的字段，再收集表的统计信息后
drop table if exists analyze_006;
create table analyze_006(id int,name clob,num int);
insert into analyze_006 values(1,'xxxxx',2);
insert into analyze_006 values(3,'yyyyy',4);
select * from analyze_006;
analyze analyze_006;
select * from pg_statistic where starelid = (select oid from pg_class where relname = 'analyze_006');
delete from analyze_006 where id=1;
analyze analyze_006;
select * from pg_statistic where starelid = (select oid from pg_class where relname = 'analyze_006');
drop table if exists analyze_006;

