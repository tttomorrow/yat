-- @testpoint: 删除行存表的索引添加on table，部分测试点合理报错
--step1:建表;expect:成功
drop table if exists t_grammar0006;
create table t_grammar0006 (a text(10), b box);
--step2:创建btree索引;expect:成功
drop index if exists  id_grammar0006;
create index id_grammar0006 on t_grammar0006 using btree(a);
--step3:删除索引添加on table;expect:成功
drop index id_grammar0006 on t_grammar0006;

--step4:创建hash索引;expect:成功
drop index if exists id_grammar0006_01;
create index id_grammar0006_01 on t_grammar0006 using hash(a);
--step5:删除索引添加on table;expect:成功
drop index id_grammar0006_01 on t_grammar0006;

--step6:创建gin索引;expect:成功
drop index if exists id_grammar0006_02;
create index id_grammar0006_02 on t_grammar0006 using gin(to_tsvector('ngram', a));
--step7:删除索引添加on table;expect:成功
drop index id_grammar0006_02 on t_grammar0006;

--step8:创建gist索引;expect:成功
drop index if exists id_grammar0006_03;
create index id_grammar0006_03 on t_grammar0006 using gist (b);
--step9:删除索引添加on table;expect:成功
drop index id_grammar0006_03 on t_grammar0006;

--step10:创建ustore表;expect:成功
drop table if exists t_grammar0006_01;
create table t_grammar0006_01 (a text(10), b box)with (storage_type=ustore);
--step11:创建ubtree索引;expect:成功
drop index if exists id_grammar0006_04;
create index id_grammar0006_04 on t_grammar0006_01 using ubtree (a);
--step12:删除索引添加on table;expect:成功
drop index id_grammar0006_04 on t_grammar0006_01;
--step13:删除索引;expect:成功
drop index if exists id_grammar0006_04 on t_grammar0006_01;
--step14:删除索引，表名不存在;expect:合理报错err
drop index id_grammar0006_04 on t_grammar0006_015689;

--step15:清理环境;expect:成功
drop table if exists t_grammar0006;
drop table if exists t_grammar0006_01;
