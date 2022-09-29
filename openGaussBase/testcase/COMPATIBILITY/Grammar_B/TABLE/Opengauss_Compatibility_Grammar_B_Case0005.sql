-- @testpoint: 修改表的压缩参数，合理报错
--step1:创建表;expect:成功
drop table if exists tb_grammar0005_01;
create table tb_grammar0005_01 (a double);

--step2:修改压缩参数;expect:报错，error:  syntax error
alter table tb_grammar0005_01 compression = zstd;
alter table tb_grammar0005_01 compression = pglz;

--step3:清理环境;expect:成功
drop table if exists tb_grammar0005_01;