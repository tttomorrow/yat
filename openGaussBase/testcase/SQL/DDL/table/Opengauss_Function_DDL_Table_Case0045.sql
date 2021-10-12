-- @testpoint: 重命名列存表中指定的列

drop table if exists table_045;
create table table_045(c_id int,name varchar2(10),time date ,sex clob)with(ORIENTATION=COLUMN);
insert into table_045 values(1,'m',to_date('2018','yyyy'),'mmmmmm');
insert into table_045 values(2,'mm',to_date('2018','yyyy'),'mmmmmm');
insert into table_045 values(3,'mmm',to_date('2018','yyyy'),'mmmmmm');
insert into table_045 values(4,'mmmm',to_date('2018','yyyy'),'mmmmmm');
select * from table_045;
ALTER TABLE  IF EXISTS table_045 REname COLUMN  time TO date;
insert into table_045 values(2,'mm',to_date('2018','yyyy'),'mmmmmm');
insert into table_045 values(3,'mmm',to_date('2018','yyyy'),'mmmmmm');
insert into table_045 values(4,'mmmm',to_date('2018','yyyy'),'mmmmmm');
select * from table_045;
drop table if exists table_045;