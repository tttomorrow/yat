-- @testpoint: 创建临时表同义词：创建不会报错，查询时，合理报错
-- @modify at: 2020-11-25
--建表
drop table if exists test_tempsyn;
CREATE TEMPORARY table test_tempsyn(id int);
--插入数据
insert into test_tempsyn values(1);
--查询
select * from test_tempsyn;
--创建临时表同义词
drop synonym if exists tmp_syn_01;
create synonym tmp_syn_01 for test_tempsyn;
--查询，报错
select * from tmp_syn_01;
--删表
drop table if exists test_tempsyn;
--删同义词
drop synonym if exists tmp_syn_01;