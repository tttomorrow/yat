-- @testpoint: json类型的分区表上创建索引:不支持，合理报错

--分区表：Json类型分区表创建成功
drop table if exists tab110;
create table tab110(id int,name varchar,message json)
partition by range(id)
(partition part_1 values less than(20),
 partition part_2 values less than(30),
 partition part_3 values less than(maxvalue));
insert into tab110 values(001,'Jane','{"age":18,"city":"xianyang"}');
insert into tab110 values(012,'Joy','{"age":19,"city":"qingdao"}');
insert into tab110 values(023,'Jack','{"age":20,"city":"xiamen"}');
insert into tab110 values(024,'Json','{"age":23,"city":"shenzhen"}');
insert into tab110 values(035,'Jim','{"age":21,"city":"shanghai"}');
select * from tab110 partition (part_1);
select * from tab110 partition (part_2);
select * from tab110 partition (part_3);

--创建索引
drop index if exists index1101;
drop index if exists index1102;
drop index if exists index1103;
drop index if exists index1104;
drop index if exists index1105;
drop index if exists index1106;
create index index1101 on tab110(message);
create index index1102 on tab110 using gist(message)global;
create index index1103 on tab110 using gist(message)local;
create index index1104 on tab110 using gin(message)global;
create index index1105 on tab110 using gin(message)local;
create unique index index1106 on tab110 using btree(message asc);

--清理数据
drop table if exists tab110;