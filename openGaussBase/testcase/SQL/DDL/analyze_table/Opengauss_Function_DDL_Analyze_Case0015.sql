-- @testpoint: analyze临时表

drop table if exists analyze_007;
create  temporary table analyze_007(id int,name clob,num int);
insert into analyze_007 values(1,'xxxxx',2);
insert into analyze_007 values(3,'yyyyy',4);
select * from analyze_007;
analyze analyze_007;
select * from pg_statistic where starelid = (select oid from pg_class where relname = 'analyze_007');
drop table if exists analyze_007;