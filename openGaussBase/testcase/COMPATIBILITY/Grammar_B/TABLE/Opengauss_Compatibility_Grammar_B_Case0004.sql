-- @testpoint: compression参数无效值测试,部分测试点合理报错
--step1:建表指定压缩参数为无效字符;expect:报错error:  unrecognized compress type
drop table if exists tb_grammar0004_01;
create table tb_grammar0004_01 (a int) compression = bz;

--step2:指定压缩参数值为无效数字;expect:报错
drop table if exists tb_grammar0004_02;
create table tb_grammar0004_02 (a int) compression = 3;

--step3:指定压缩参数值为正常数字;expect:报错，不支持数字
drop table if exists tb_grammar0004_03;
create table tb_grammar0004_03 (a int) compression = 1;
drop table if exists tb_grammar0004_04;
create table tb_grammar0004_04 (a int) compression = 2;

--step4:建表指定压缩参数为不加引号的none;expect:成功
drop table if exists tb_grammar0004_05;
create table tb_grammar0004_05 (a int) compression = none;

--step5:清理环境;expect:成功
drop table if exists tb_grammar0004_05;