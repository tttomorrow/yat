-- @testpoint: 收集表的统计信息并输出表的相关信息

drop table if exists analyze_001;
create table analyze_001(c_id int,name varchar2(10),time date ,sex clob);
insert into analyze_001 values(1,'m',to_date('2018','yyyy'),'mmmmmm');
select c_id,name,sex from analyze_001 order by c_id;
analyze VERBOSE analyze_001;
select * from pg_statistic where starelid = (select oid from pg_class where relname = 'analyze_001');
drop table if exists analyze_001;