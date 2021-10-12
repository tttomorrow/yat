-- @testpoint: 行存表使用数据类型为jsonb的列创建索引:不支持gist索引，合理报错

--行存表：创建索引
drop table if exists tab116;
create table tab116(id int,name varchar,message jsonb);
insert into tab116 values(001,'Jane','{"age":18,"city":"xianyang"}');
insert into tab116 values(012,'Joy','{"age":19,"city":"qingdao"}');
insert into tab116 values(023,'Jack','{"age":20,"city":"xiamen"}');
insert into tab116 values(004,'Json','{"age":23,"city":"shenzhen"}');
insert into tab116 values(005,'Jim','{"age":21,"city":"shanghai"}');
select * from  tab116;
drop index if exists index1161;
drop index if exists index1162;
drop index if exists index1163;
drop index if exists index1164;
create index index1161 on tab116(message);
create index index1162 on tab116 using gist(message);
create index index1163 on tab116 using gin(message);
create unique index index1164 on tab116 using btree(message asc);

--清理数据
drop index if exists index1161;
drop index if exists index1162;
drop index if exists index1163;
drop index if exists index1164;
drop table if exists tab116;