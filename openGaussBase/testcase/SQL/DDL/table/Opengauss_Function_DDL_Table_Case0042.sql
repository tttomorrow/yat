-- @testpoint: alter列存表设置单个字段的收集目标SET STATISTICS


drop table if exists analyze_table_042;
create table analyze_table_042(c_id int,name varchar2(10),time date ,sex clob)with(ORIENTATION=COLUMN);
insert into analyze_table_042 values(1,'m',to_date('2018','yyyy'),'mmmmmm');
insert into analyze_table_042 values(2,'mm',to_date('2018','yyyy'),'mmmmmm');
insert into analyze_table_042 values(3,'mmm',to_date('2018','yyyy'),'mmmmmm');
insert into analyze_table_042 values(4,'mmmm',to_date('2018','yyyy'),'mmmmmm');
alter table analyze_table_042 ALTER COLUMN name SET STATISTICS PERCENT 50;
alter table analyze_table_042 ADD  STATISTICS ((c_id, name));
alter table analyze_table_042 DELETE STATISTICS ((c_id, name));
analyze   analyze_table_042;
drop table if exists analyze_table_042;