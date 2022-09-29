-- @testpoint: 删除列存表的索引添加on table
--step1:建表;expect:成功
drop table if exists t_plugin0007;
create table t_plugin0007 (a text(10), b int) with(orientation=column);

--step2:创建psort索引;expect:成功
drop index if exists id_plugin0007_01;
create index id_plugin0007_01 on t_plugin0007 using psort(a);

--step3:删除索引,添加on table;expect:成功
drop index id_plugin0007_01 on  id_plugin0007;

--step4:创建btree索引;expect:成功
drop index if exists id_plugin0007_02;
create index id_plugin0007_02 on t_plugin0007 using btree(a);

--step5:删除索引,添加on table;expect:成功
drop index id_plugin0007_02 on id_plugin0007;

--step6:创建gin索引;expect:成功
drop index if exists id_plugin0007_03;
create index id_plugin0007_03 on t_plugin0007 using gin(to_tsvector('ngram', a));

--step7:删除索引,添加on table;expect:成功
drop index id_plugin0007_03 on id_plugin0007;

--step8:清理环境;expect:成功
drop table if exists t_plugin0007;
