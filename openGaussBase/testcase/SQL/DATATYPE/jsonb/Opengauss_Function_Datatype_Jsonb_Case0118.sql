-- @testpoint: jsonb不支持作为分区表的分区键,合理报错

--分区表：jsonb不支持作为分区表的分区键
drop table if exists tab1181;
create table tab1181(id int,name varchar,message jsonb)
partition by range(message)
(partition part_1 values less than(20),
 partition part_2 values less than(30),
 partition part_3 values less than(maxvalue));

--分区表：jsonb不作为分区表的分区键，分区表创建成功
drop table if exists tab1182;
create table tab1182(id int,name varchar,message jsonb)
partition by range(id)
(partition part_1 values less than(20),
 partition part_2 values less than(30),
 partition part_3 values less than(maxvalue));
insert into tab1182 values(001,'Jane','{"age":18,"city":"xianyang"}');
insert into tab1182 values(012,'Joy','{"age":19,"city":"qingdao"}');
insert into tab1182 values(023,'Jack','{"age":20,"city":"xiamen"}');
insert into tab1182 values(024,'json','{"age":23,"city":"shenzhen"}');
insert into tab1182 values(035,'Jim','{"age":21,"city":"shanghai"}');
select * from tab1182 partition (part_1);
select * from tab1182 partition (part_2);
select * from tab1182 partition (part_3);

--清理数据
drop table if exists tab1181;
drop table if exists tab1182;