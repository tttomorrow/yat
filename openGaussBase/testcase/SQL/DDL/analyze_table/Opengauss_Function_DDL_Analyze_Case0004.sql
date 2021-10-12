-- @testpoint: 添加表的column_1、column_2列的多列统计信息声明
drop table if exists analyze_002;
create table analyze_002(c_id int,name varchar2(10),time date ,sex varchar2(20));
insert into analyze_002 values(1,'mm',to_date('2018','yyyy'),'mm');
insert into analyze_002 values(2,'m',to_date('2018','yyyy'),'m');
insert into analyze_002 values(3,'mmmm',to_date('2018','yyyy'),'mmmmmm');
select * from analyze_002 order by c_id;
analyze analyze_002  ((c_id, name));
select * from pg_statistic where starelid = (select oid from pg_class where relname = 'analyze_002');
alter table  analyze_002 add statistics ((c_id, name));
analyze analyze_002;
select * from pg_statistic where starelid = (select oid from pg_class where relname = 'analyze_002');
select c_id,name from analyze_002 order by c_id;
drop table if exists analyze_002;