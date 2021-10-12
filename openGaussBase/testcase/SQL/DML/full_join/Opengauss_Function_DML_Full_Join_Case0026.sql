--  @testpoint:两张表使用full join查询，指定连接条件使用using,对应的列名不同，合理报错
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
--表1和表2使用full join查询,连接条件使用using，合理报错
select * from person per full join address ad using(personcode);
--using条件中，其中有一列列名不匹配，合理报错
select * from person per full join address ad using(addresscode,personcode);
--删表
drop table if exists person;
drop table if exists address;