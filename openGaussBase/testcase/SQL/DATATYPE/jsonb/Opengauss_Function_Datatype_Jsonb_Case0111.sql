-- @testpoint: json类型的临时表上创建索引:不支持，合理报错

--建本地临时表
drop table if exists tab111 cascade;
create local temporary table tab111(id int,name varchar,message json);

--插入数据
insert into tab111 values(001,'Jane','{"age":18,"city":"xianyang"}');
insert into tab111 values(012,'Joy','{"age":19,"city":"qingdao"}');
insert into tab111 values(023,'Jack','{"age":20,"city":"xiamen"}');
insert into tab111 values(004,'Json','{"age":23,"city":"shenzhen"}');
insert into tab111 values(005,'Jim','{"age":21,"city":"shanghai"}');

--创建索引，不支持，合理报错
drop index if exists index1111;
drop index if exists index1112;
drop index if exists index1113;
drop index if exists index1114;
create index index1111 on tab111(message);
create index index1112 on tab111 using gist(message);
create index index1113 on tab111 using gin(message);
create unique index index1114 on tab111 using btree(message asc);

--建全局临时表
drop table if exists tab1112 cascade;
create global temporary table tab1112(id int,name varchar,message json);

--插入数据
insert into tab1112 values(001,'Jane','{"age":18,"city":"xianyang"}');
insert into tab1112 values(012,'Joy','{"age":19,"city":"qingdao"}');
insert into tab1112 values(023,'Jack','{"age":20,"city":"xiamen"}');
insert into tab1112 values(004,'Json','{"age":23,"city":"shenzhen"}');
insert into tab1112 values(005,'Jim','{"age":21,"city":"shanghai"}');

--创建索引，不支持，合理报错
drop index if exists index11121;
drop index if exists index11122;
drop index if exists index11123;
drop index if exists index11124;
create index index11121 on tab1112(message);
create index index11122 on tab1112 using gist(message);
create index index11123 on tab1112 using gin(message);
create unique index index11124 on tab1112 using btree(message asc);

--清理数据
drop table if exists tab111 cascade;
drop table if exists tab1112 cascade;
