--  @testpoint:执行序列的最大值测试
drop SEQUENCE if exists test_seq1;
create SEQUENCE test_seq1 INCREMENT 2;
select sequence_name,max_value from test_seq1 where sequence_name = 'test_seq1';
--删除序列
drop SEQUENCE test_seq1;
drop SEQUENCE if exists test_seq2;
create SEQUENCE test_seq2 INCREMENT 2 NO MAXVALUE;
select sequence_name,max_value from test_seq2 where sequence_name = 'test_seq2';
--删除序列
drop SEQUENCE test_seq2;
--创建递增序列，声明minvalue，查询序列的最大值(100)
drop SEQUENCE if exists test_seq3;
create SEQUENCE test_seq3 INCREMENT 2 MAXVALUE 100;
select sequence_name,max_value,start_value from test_seq3 where sequence_name = 'test_seq3';
--调用函数一次（1）,序列的起始值,对于递增序列为1
select nextval('test_seq3');
--删除序列
drop SEQUENCE test_seq3;
--创建递减序列，没有声明maxvalue，查询序列的最大(-1)
drop SEQUENCE if exists test_seq4;
create SEQUENCE test_seq4 INCREMENT -2;
select sequence_name,max_value from test_seq4 where sequence_name = 'test_seq4';
--删除序列
drop SEQUENCE test_seq4;
--创建递减序列，声明NO MAXVALUE，查询序列的最大值(-1)
drop SEQUENCE if exists test_seq5;
create SEQUENCE test_seq5 INCREMENT -2 NO MAXVALUE;
select sequence_name,max_value from test_seq5 where sequence_name = 'test_seq5';
--删除序列
drop SEQUENCE test_seq5;
--创建递减序列，声明NOMAXVALUE，查询序列的最大值(-1)
drop SEQUENCE if exists test_seq6;
create SEQUENCE test_seq6 INCREMENT -2 NOMAXVALUE;
select sequence_name,max_value from test_seq6 where sequence_name = 'test_seq6';
--删除序列
drop SEQUENCE test_seq6;