-- @testpoint: 临时表使用数据类型为jsonb的列创建索引，gist索引不支持，合理报错

--建本地临时表
drop table if exists tab122 cascade;
create local temporary table tab122(id int,name varchar,message jsonb);

--插入数据
insert into tab122 values(001,'Jane','{"age":18,"city":"xianyang"}');
insert into tab122 values(012,'Joy','{"age":19,"city":"qingdao"}');
insert into tab122 values(023,'Jack','{"age":20,"city":"xiamen"}');
insert into tab122 values(004,'json','{"age":23,"city":"shenzhen"}');
insert into tab122 values(005,'Jim','{"age":21,"city":"shanghai"}');

--创建索引，gist索引不支持，合理报错
drop index if exists index12211;
drop index if exists index12212;
drop index if exists index12213;
drop index if exists index12214;
create index index12211 on tab122(message);
create index index12212 on tab122 using gin(message);
create unique index index12213 on tab122 using btree(message asc);
create index index12214 on tab122 using gist(message);

--建全局临时表
drop table if exists tab1222 cascade;
create global temporary table tab1222(id int,name varchar,message jsonb);

--插入数据
insert into tab1222 values(001,'Jane','{"age":18,"city":"xianyang"}');
insert into tab1222 values(012,'Joy','{"age":19,"city":"qingdao"}');
insert into tab1222 values(023,'Jack','{"age":20,"city":"xiamen"}');
insert into tab1222 values(004,'Json','{"age":23,"city":"shenzhen"}');
insert into tab1222 values(005,'Jim','{"age":21,"city":"shanghai"}');

--创建索引，gist索引不支持，合理报错
drop index if exists index12221;
drop index if exists index12222;
drop index if exists index12223;
drop index if exists index12224;
create index index12221 on tab1222(message);
create index index12222 on tab1222 using gin(message);
create unique index index12223 on tab1222 using btree(message asc);
create index index12224 on tab1222 using gist(message);

--清理数据
drop index if exists index12211;
drop index if exists index12212;
drop index if exists index12213;
drop index if exists index12214;
drop index if exists index12221;
drop index if exists index12222;
drop index if exists index12223;
drop index if exists index12224;
drop table if exists tab122 cascade;
drop table if exists tab1222 cascade;
