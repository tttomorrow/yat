-- @testpoint: 行存表使用数据类型为json的列创建索引:不支持gist索引，合理报错

--行存表：创建索引
drop table if exists tab107;
create table tab107(id int,name varchar,message json);
insert into tab107 values(001,'Jane','{"age":18,"city":"xianyang"}');
insert into tab107 values(012,'Joy','{"age":19,"city":"qingdao"}');
insert into tab107 values(023,'Jack','{"age":20,"city":"xiamen"}');
insert into tab107 values(004,'Json','{"age":23,"city":"shenzhen"}');
insert into tab107 values(005,'Jim','{"age":21,"city":"shanghai"}');
select * from  tab107;
drop index if exists index1071;
drop index if exists index1072;
drop index if exists index1073;
drop index if exists index1074;
create index index1071 on tab107(message);
create index index1072 on tab107 using gist(message);
create index index1073 on tab107 using gin(message);
create unique index index1074 on tab107 using btree(message asc);

--清理数据
drop index if exists index1071;
drop index if exists index1072;
drop index if exists index1073;
drop index if exists index1074;
drop table if exists tab107 cascade;

