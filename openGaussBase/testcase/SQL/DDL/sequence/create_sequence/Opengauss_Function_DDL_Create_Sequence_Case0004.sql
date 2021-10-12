--  @testpoint:创建序列，步长测试
--testpoint1:创建序列，指定步长为正数
drop SEQUENCE if exists test_seq1;
create SEQUENCE test_seq1 INCREMENT 2;
--查看步长信息
select sequence_name,increment_by from test_seq1 where sequence_name = 'test_seq1';
--调用函数一次（1）
select nextval('test_seq1');
--调用函数两次（3）
select nextval('test_seq1');
--testpoint2:创建序列，指定步长为负数
drop SEQUENCE if exists test_seq2;
create SEQUENCE test_seq2 INCREMENT by -2;
--调用函数一次（-1）
select nextval('test_seq2');
--调用函数两次（-3）
select nextval('test_seq2');
--testpoint3:创建序列，指定步长为0，合理报错
drop SEQUENCE if exists test_seq3;
create SEQUENCE test_seq3 INCREMENT by 0;
--删除序列
drop SEQUENCE test_seq1;
drop SEQUENCE test_seq2;