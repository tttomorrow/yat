--  @testpoint:重命名枚举类型的一个标签值
--创建枚举类型
drop type if exists bugstatus3 cascade;
CREATE TYPE bugstatus3 AS ENUM ('create', 'modify', 'closed');
--重命名枚举类型的一个标签值,枚举值存在
ALTER TYPE bugstatus3 RENAME VALUE 'create' TO 'delete';
--建表
drop table if exists test_t6 cascade;
create table test_t6 (id int,d bugstatus3);
--插入数据
insert into test_t6 values(1,'delete');
--删表
drop table test_t6 cascade;
--删除类型
drop type bugstatus3 cascade;