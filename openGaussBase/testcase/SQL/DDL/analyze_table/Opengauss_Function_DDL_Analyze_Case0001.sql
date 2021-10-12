-- @testpoint: ANALYZE  TABLE (全表)
drop table if exists analyze_001;
create table analyze_001(c_id int,name varchar2(10),time date ,sex clob);
insert into analyze_001 values(1,'m',to_date('2018','yyyy'),'mmmmmm');
insert into analyze_001 values(2,'mm',to_date('2018','yyyy'),'mmmmmm');
insert into analyze_001 values(3,'mmm',to_date('2018','yyyy'),'mmmmmm');
insert into analyze_001 values(4,'mmmm',to_date('2018','yyyy'),'mmmmmm');
analyze analyze_001;
select * from pg_statistic where starelid = (select oid from pg_class where relname = 'analyze_001');
drop table if exists analyze_001;