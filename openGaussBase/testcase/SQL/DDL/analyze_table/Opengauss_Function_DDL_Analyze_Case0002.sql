-- @testpoint: ANALYZE TABLE (表的多列统计信息)
drop table if exists analyze_001;
create table analyze_001(c_id int,name varchar2(10),time date ,sex clob);
insert into analyze_001 values(1,'m',to_date('2018','yyyy'),'mmmmmm');
insert into analyze_001 values(2,'mmm',to_date('2018','yyyy'),'mmmmmm');
insert into analyze_001 values(3,'mmmmm',to_date('2018','yyyy'),'mmmmmm');
select c_id,name,sex from analyze_001 order by c_id;
analyze analyze_001  ((c_id, name));
select * from pg_statistic where starelid = (select oid from pg_class where relname = 'analyze_001');
analyze analyze_001;
drop table if exists analyze_001;


