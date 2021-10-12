-- @testpoint: 行存表使用数据类型为jsonb的列创建索引:gist索引不支持，合理报错

--行存表
drop table if exists tab112;
create table tab112(id int,name varchar,message jsonb);
insert into tab112 values(001,'Jane','{"age":18,"city":"xianyang"}');
insert into tab112 values(012,'Joy','{"age":19,"city":"qingdao"}');
insert into tab112 values(023,'Jack','{"age":20,"city":"xiamen"}');
insert into tab112 values(004,'Json','{"age":23,"city":"shenzhen"}');
insert into tab112 values(005,'Jim','{"age":21,"city":"shanghai"}');
select * from  tab112;

--创建索引：btree,gin
drop index if exists index1121;
drop index if exists index1122;
drop index if exists index1123;
drop index if exists index1124;
drop index if exists index1125;
drop index if exists index1126;
create index index1121 on tab112(message);
create index index1123 on tab112 using gin(message);
create unique index index1124 on tab112 using btree(message asc);
create index index1125 on tab112 using gin ((message ->'{"age": 18, "city": "xianyang"}'));
create index index1126 on tab112 using  btree ((message ->'{"age": 18, "city": "xianyang"}'));

--gist索引不支持，合理报错
create index index1122 on tab112 using gist(message);

--清理数据
drop index if exists index1121;
drop index if exists index1122;
drop index if exists index1123;
drop index if exists index1124;
drop index if exists index1125;
drop index if exists index1126;
drop table if exists tab112;