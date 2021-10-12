-- @testpoint: create table时复制满足where后面条件的表结构


DROP TABLE IF EXISTS tools;
create table tools(wide number(10,0),highs number(20,0));
insert into tools values(10,24);
commit;
drop table if exists tools_1;
create table tools_1 as select wide as w from tools;
select * from tools_1;
DROP TABLE IF EXISTS tools_2;
create table tools_2 as select * from tools where 1>2;
select * from tools_2;
DROP TABLE IF EXISTS tools;
drop table if exists tools_1;
DROP TABLE IF EXISTS tools_2;