--  @testpoint:为枚举类型增加一个新值
--创建枚举类型
drop type if exists bugstatus cascade;
CREATE TYPE bugstatus AS ENUM ('create', 'modify', 'closed');
--为枚举类型增加一个新值,在已有标签值之前
ALTER TYPE bugstatus ADD VALUE 'insert' BEFORE 'create';
--建表
drop table if exists test_t5 cascade;
create table test_t5 (id int,d bugstatus);
--插入数据
insert into test_t5 values(1,'modify');
insert into test_t5 values(1,'insert');
--查询表信息
select * from test_t5;
--为枚举类型增加一个新值,在已有标签值之后
ALTER TYPE bugstatus ADD VALUE 'update' after 'closed';
--插入数据
insert into test_t5 values(1,'update');
--删表
drop table if exists test_t5 cascade;
--删除类型
drop type if exists bugstatus cascade;