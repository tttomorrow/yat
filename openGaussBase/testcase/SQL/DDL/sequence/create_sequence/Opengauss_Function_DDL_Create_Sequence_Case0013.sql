--  @testpoint:创建序列，关联表和序列所在模式不同，合理报错
--创建schema
drop schema if exists test1_schema cascade;
create schema test1_schema;
--test_schema下建表
drop table if exists test1_schema.customer_address;
CREATE TABLE test1_schema.customer_address
(
  ca_address_sk             integer               not null,
  ca_address_id             char(16)              not null);
--创建与表关联的序列（public下创建序列）,合理报错，ERROR:  sequence must be in same schema as table it is linked to
drop SEQUENCE if exists test2_serial;
CREATE SEQUENCE test2_serial START 101 CACHE 20 OWNED BY test1_schema.customer_address.ca_address_sk;
--删除表
drop table test1_schema.customer_address;
--删除schema
drop schema test1_schema;