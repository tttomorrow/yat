-- @testpoint: 插入数值类型，唯一约束列数据重复，合理报错
-- @modify at: 2020-11-16
--建表
DROP TABLE if exists t_uint32;
CREATE TABLE t_uint32(c1 int,c2 integer);
--创建唯一索引
drop index if exists idx_t_uint32;
create unique index idx_t_uint32 on t_uint32(c2);
--插入数据
insert into t_uint32 values(1, 10);
--再次插入数据，合理报错
insert  into t_uint32 values(2, 10);
--删表
DROP TABLE if exists t_uint32 cascade;

