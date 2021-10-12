--  @testpoint:创建序列，OWNED BY测试
--创建与表关联的序列
drop table if exists customer_address;
CREATE TABLE customer_address
(
  ca_address_sk             integer               not null,
  ca_address_id             char(16)              not null);
--创建序列，序列和一个表的指定字段进行关联
drop SEQUENCE if exists test_serial1;
CREATE SEQUENCE test_serial1 START 101 CACHE 20 OWNED BY customer_address.ca_address_sk;
--插入数据
insert into customer_address values(1,'kili');
--插入数据，合理报错，在插入数据时在该列上不会产生自增序列
insert into customer_address values(default,'kili');
--删除表字段
alter table customer_address drop  ca_address_sk;
--查询关联序列，不存在，合理报错（删除那个字段或其所在表的时候会自动删除已关联的序列）
select * from test_serial1;
--删除表
drop table customer_address;
