--  @testpoint:执行序列的最小值测试
--创建递增序列，没有声明minvalue，查询序列的最小值(1)
drop SEQUENCE if exists test_seq1;
create SEQUENCE test_seq1 INCREMENT 2;
select sequence_name,min_value from test_seq1 where sequence_name = 'test_seq1';
--删除序列
drop SEQUENCE test_seq1;
--创建递增序列,声明了NO MINVALUE,查询序列的最小值(1)
drop SEQUENCE if exists test_seq2;
create SEQUENCE test_seq2 INCREMENT 2 NO MINVALUE ;
select sequence_name,min_value from test_seq2 where sequence_name = 'test_seq2';
--删除序列
drop SEQUENCE test_seq2;
--创建递增序列，声明minvalue，查询序列的最小值(5)
drop SEQUENCE if exists test_seq3;
create SEQUENCE test_seq3 INCREMENT 2 MINVALUE 5;
select sequence_name,min_value,start_value from test_seq3 where sequence_name = 'test_seq3';
--调用函数一次（5）,序列的起始值,对于递增序列为minvalue
select nextval('test_seq3');
--删除序列
drop SEQUENCE test_seq3;
drop SEQUENCE if exists test_seq4;
create SEQUENCE test_seq4 INCREMENT -2;
select sequence_name,min_value from test_seq4 where sequence_name = 'test_seq4';
--删除序列
drop SEQUENCE test_seq4;
drop SEQUENCE if exists test_seq5;
create SEQUENCE test_seq5 INCREMENT -2 NO MINVALUE;
select sequence_name,min_value from test_seq5 where sequence_name = 'test_seq5';
--删除序列
drop SEQUENCE test_seq5;
drop SEQUENCE if exists test_seq6;
create SEQUENCE test_seq6 INCREMENT -2 NOMINVALUE;
select sequence_name,min_value from test_seq6 where sequence_name = 'test_seq6';
--删除序列
drop SEQUENCE test_seq6;