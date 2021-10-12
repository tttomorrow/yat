-- @testpoint: 行存表使用数据类型为jsonb的列创建索引:gist索引不支持，合理报错

--行存表
drop table if exists tab119;
create table tab119(id int,name varchar,message jsonb);
insert into tab119 values(001,'Jane','{"age":18,"city":"xianyang"}');
insert into tab119 values(012,'Joy','{"age":19,"city":"qingdao"}');
insert into tab119 values(023,'Jack','{"age":20,"city":"xiamen"}');
insert into tab119 values(004,'Json','{"age":23,"city":"shenzhen"}');
insert into tab119 values(005,'Jim','{"age":21,"city":"shanghai"}');
select * from  tab119;

--创建索引：btree,gin
drop index if exists index1191;
drop index if exists index1192;
drop index if exists index1193;
drop index if exists index1194;
drop index if exists index1195;
drop index if exists index1196;
drop index if exists unique_index1197;
drop index if exists exp_index1;
drop index if exists exp_index2;
drop index if exists exp_index3;
create index index1191 on tab119(message);
create index index1193 on tab119 using gin(message);
create unique index index1194 on tab119 using btree(message asc);
create index index1195 on tab119 using gin ((message ->'{"age": 18, "city": "xianyang"}'));
create index index1196 on tab119 using  btree ((message ->'{"age": 18, "city": "xianyang"}'));
create unique index unique_index1197 on tab119 using btree(message asc);
create index exp_index1 on tab119 ((message @>'{"age": 18, "city": "xianyang"}'));
create index exp_index3 on tab119 (message) where message>'{"age":18}';
select relname from pg_class where relname='index1195';

--gist索引不支持，合理报错
create index index1192 on tab119 using gist(message);

--清理数据
drop index if exists index1191;
drop index if exists index1192;
drop index if exists index1193;
drop index if exists index1194;
drop index if exists index1195;
drop index if exists index1196;
drop index if exists unique_index1197;
drop index if exists exp_index1;
drop index if exists exp_index2;
drop index if exists exp_index3;
drop table if exists tab119 cascade;