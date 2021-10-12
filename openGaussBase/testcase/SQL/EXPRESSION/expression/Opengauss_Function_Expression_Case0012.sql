--  @testpoint:EXISTS/NOT EXISTS
--EXISTS的参数是一个任意的SELECT语句,或者说子查询。
--系统对子查询进行运算以判断它是否返回行。
--如果它至少返回一行,则EXISTS结果就为"真"；如果子查询没有返回任何行, EXISTS的结果是"假"。
--这个子查询通常只是运行到能判断它是否可以生成至少一行为止,而不是等到全部结束

--建表
DROP TABLE if exists test_expression_12_01 cascade;
DROP TABLE if exists test_expression_12_02 cascade;
CREATE TABLE test_expression_12_01
(
    c_id            INTEGER               NOT NULL,
    c_name            CHAR(16)              NOT NULL,
    c_class                VARCHAR(20)
);

CREATE TABLE test_expression_12_02
(
    c_gradeid            INTEGER               NOT NULL,
    c_id            INTEGER               NOT NULL,
    c_grade         INTEGER,
    c_subject       varchar
);
insert into test_expression_12_01 values(101,'zhangsan1','101');
insert into test_expression_12_01 values(102,'zhangsan2','101');
insert into test_expression_12_01 values(103,'zhangsan3','101');
insert into test_expression_12_01 values(104,'zhangsan4','102');
insert into test_expression_12_01 values(105,'zhangsan5','102');
insert into test_expression_12_01 values(106,'zhangsan6','103');
insert into test_expression_12_02 values(1001,101,80,'语');
insert into test_expression_12_02 values(1002,102,90,'语');
insert into test_expression_12_02 values(1003,103,75,'语');
insert into test_expression_12_02 values(1004,104,58,'语');
insert into test_expression_12_02 values(1005,105,96,'语');
insert into test_expression_12_02 values(1006,106,68,'语');
insert into test_expression_12_02 values(1007,101,68,'数');
insert into test_expression_12_02 values(1008,102,85,'数');
insert into test_expression_12_02 values(1009,103,85,'数');
insert into test_expression_12_02 values(1010,104,54,'数');
insert into test_expression_12_02 values(1011,105,75,'数');
insert into test_expression_12_02 values(1012,106,45,'数');
insert into test_expression_12_02 values(1013,101,85,'英');
insert into test_expression_12_02 values(1014,102,54,'英');
insert into test_expression_12_02 values(1015,103,68,'英');
insert into test_expression_12_02 values(1016,104,86,'英');
insert into test_expression_12_02 values(1017,105,55,'英');
insert into test_expression_12_02 values(1018,106,97,'英');
insert into test_expression_12_02 values(1019,106,100,null);

--exists/not exists为真,返回一行和多行
SELECT c_name,c_class FROM test_expression_12_01
WHERE EXISTS (SELECT c_grade FROM test_expression_12_02 WHERE c_id = test_expression_12_01.c_id and c_grade >85);
SELECT c_name,c_class FROM test_expression_12_01
WHERE EXISTS (SELECT c_grade,c_subject FROM test_expression_12_02 WHERE c_id = test_expression_12_01.c_id and c_grade >85);

--exists/not exists为假,无返回
SELECT c_name,c_class FROM test_expression_12_01
WHERE EXISTS (SELECT c_subject FROM test_expression_12_02 WHERE c_id = test_expression_12_01.c_id and c_grade >99);
SELECT c_name,c_class FROM test_expression_12_01
WHERE EXISTS (SELECT c_grade,c_subject FROM test_expression_12_02 WHERE c_id = test_expression_12_01.c_id and c_grade >99);

--exists/not exists为返回一行但值为null
SELECT c_name,c_class FROM test_expression_12_01
WHERE EXISTS (SELECT c_subject FROM test_expression_12_02 WHERE c_id = test_expression_12_01.c_id and c_grade =100);
SELECT c_name,c_class FROM test_expression_12_01
WHERE EXISTS (SELECT c_grade,c_subject FROM test_expression_12_02 WHERE c_id = test_expression_12_01.c_id and c_grade =100);

--环境清理
DROP TABLE if exists test_expression_12_01 cascade;
DROP TABLE if exists test_expression_12_02 cascade;