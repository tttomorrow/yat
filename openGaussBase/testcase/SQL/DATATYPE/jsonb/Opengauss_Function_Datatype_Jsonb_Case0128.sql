-- @testpoint: 对数据时jsonb的表进行DML操作

drop table if exists tab128;
create table tab128(id int,name varchar,message jsonb,number text);
insert into tab128 values(001,'Jane','{"age":18,"city":"xianyang"}',1596);
insert into tab128 values(012,'Joy','{"age":19,"city":"qingdao"}',2586);
insert into tab128 values(023,'Jack','{"age":20,"city":"xiamen"}',85236);
insert into tab128 values(004,'Json','{"age":23,"city":"shenzhen"}',45632);
insert into tab128 values(005,'Jim','{"age":21,"city":"shanghai"}',635486);
select * from  tab128;

--update
update tab128 set number = 888888 where id = 012;
select * from  tab128;
update tab128 set number = 888888;
select * from  tab128;

--delete
delete from tab128 where id < 10;
select * from  tab128;
delete from tab128;
select * from  tab128;
--truncate
insert into tab128 values(001,'Jane','{"age":18,"city":"xianyang"}',1596);
insert into tab128 values(012,'Joy','{"age":19,"city":"qingdao"}',2586);
insert into tab128 values(023,'Jack','{"age":20,"city":"xiamen"}',85236);
insert into tab128 values(004,'Json','{"age":23,"city":"shenzhen"}',45632);
insert into tab128 values(005,'Jim','{"age":21,"city":"shanghai"}',635486);
select * from  tab128;
truncate table tab128;
select * from  tab128;
--删除表
drop table if exists tab128;

