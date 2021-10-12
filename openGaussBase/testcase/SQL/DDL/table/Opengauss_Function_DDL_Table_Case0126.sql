-- @testpoint: 创建列类型为布尔类型的表
drop table if exists table_1;
create table table_1(a BOOLEAN,b BOOLEAN,c BOOLEAN,d int);
insert into table_1 values(true,false,null,1);
insert into table_1 values('t','f',null,21);
insert into table_1 values('y','n',null,21);
insert into table_1 values('yes','no',null,21);
insert into table_1 values(1,0,null,21);
insert into table_1 values(0);
insert into table_1 values(32768);
select * from table_1;
drop table if exists table_1;
