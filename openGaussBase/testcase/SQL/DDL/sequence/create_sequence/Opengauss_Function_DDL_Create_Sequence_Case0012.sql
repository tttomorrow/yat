--  @testpoint:创建序列，测试缺省值为OWNED BY NONE
--创建表
drop table if exists customer_address1;
CREATE TABLE customer_address1
(
  ca_address_sk             integer               not null,
  ca_address_id             char(16)              not null);
--创建序列，序列和一个表的指定字段不进行关联
drop SEQUENCE if exists test1_serial;
CREATE SEQUENCE test1_serial START 101 CACHE 20 OWNED BY none;
--插入数据
insert into customer_address1 values(1,'kili');
--插入数据，合理报错，在插入数据时在该列上不会产生自增序列
insert into customer_address1 values(default,'kili');
--删除表字段
alter table customer_address1 drop ca_address_sk;
--查询序列，序列存在
select sequence_name from test1_serial where sequence_name = 'test1_serial';
--删除表
drop table customer_address1;
--查询序列，序列依然存在
select sequence_name from test1_serial where sequence_name = 'test1_serial';
--删除序列
drop SEQUENCE test1_serial;