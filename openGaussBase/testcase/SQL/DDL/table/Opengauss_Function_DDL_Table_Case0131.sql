-- @testpoint: 创建列类型为字符类型clob的表
drop table if exists table_2;
create table table_2(a CLOB);
insert into table_2 values('1232');
insert into table_2 values('qewerr');
insert into table_2 values('你好');
select * from table_2;
drop table if exists table_2;
