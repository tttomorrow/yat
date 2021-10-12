--  @testpoint:两张表使用full join连接查询，(full outer join)返回结果为两个表的并集，连接字段不相等的部分为NULL
--建表1
drop table if exists person;
create table person(personcode int,personname varchar(20),addresscode int);
--插入数据
insert into person values(1,'小赵',1);
insert into person values(2,'小钱',2);
insert into person values(3,'赵四',3);
insert into person values(4,'孙晔',4);
insert into person values(5,'周瑜',6);
--建表2
drop table if exists address;
create table address(addresscode int,addressname varchar(20));
--插入数据
insert into address values(1,'北京');
insert into address values(2,'上海');
insert into address values(3,'广州');
insert into address values(4,'深圳');
insert into address values(5,'上海');
--表1和表2使用full join连接查询
select * from person per full join address ad on per.addresscode = ad.addresscode;
select * from person per full outer join address ad on per.addresscode = ad.addresscode;
--删表
drop table if exists person;
drop table if exists address;