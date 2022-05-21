-- @testpoint: 分区表DDL回滚，使用全局分区索引扫描数据不丢失，和全表扫描数据结果一致

--step1:创建范围分区表;expect:成功
drop table if exists t_index_0257;
create table t_index_0257 (id int, name varchar2(100))
partition by range (id)
(
partition t_index_0257_01 values less than (10),
partition t_index_0257_02 values less than (100)
);

--step2:范围分区表创建全局索引;expect:成功
create unique index i_index_0257 on t_index_0257 (id) global;

--step3:插入数据;expect:成功
insert into t_index_0257 values (1,'a'),(10,'b');

--step4:使用全局索引扫描数据;expect:成功
select /*+ indexscan(t_index_0257 i_index_0257) */ * from t_index_0257 where id < 200;

--step5:开启事务，删除分表，增加分表，插入数据并回滚;expect:成功
begin;
alter table t_index_0257 drop partition t_index_0257_02 update global index;
alter table t_index_0257 add partition t_index_0257_02 end (100);
insert into t_index_0257 values (10,'bb');
rollback;
/

--step6:使用全局索引扫描数据及全表扫描数据;expect:成功，结果一致
select /*+ indexscan(t_index_0257 i_index_0257) */ * from t_index_0257 where id < 200;
select * from t_index_0257 where id < 200;

--step7:清理环境;expect:成功
drop index if exists i_index_0257;
drop table if exists t_index_0257_01;
drop table if exists t_index_0257_02;
drop table if exists t_index_0257;

