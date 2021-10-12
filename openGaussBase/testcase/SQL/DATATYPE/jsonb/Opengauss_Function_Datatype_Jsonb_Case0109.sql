-- @testpoint: Json不支持作为分区表的分区键,合理报错

--分区表：Json不支持作为分区表的分区键
drop table if exists tab1091;
create table tab1091(id int,name varchar,message json)
partition by range(message)
(partition part_1 values less than(20),
 partition part_2 values less than(30),
 partition part_3 values less than(maxvalue));
drop table if exists tab1091;

--分区表：Json不作为分区表的分区键，分区表创建成功
drop table if exists tab1092;
create table tab1092(id int,name varchar,message json)
partition by range(id)
(partition part_1 values less than(20),
 partition part_2 values less than(30),
 partition part_3 values less than(maxvalue));
insert into tab1092 values(001,'Jane','{"age":18,"city":"xianyang"}');
insert into tab1092 values(012,'Joy','{"age":19,"city":"qingdao"}');
insert into tab1092 values(023,'Jack','{"age":20,"city":"xiamen"}');
insert into tab1092 values(024,'Json','{"age":23,"city":"shenzhen"}');
insert into tab1092 values(035,'Jim','{"age":21,"city":"shanghai"}');
select * from tab1092 partition (part_1);
select * from tab1092 partition (part_2);
select * from tab1092 partition (part_3);

--清理数据
drop table if exists tab1091;
drop table if exists tab1092;