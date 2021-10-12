-- @testpoint: all 合理报错
--右边是一个圆括弧括起来的子查询，它必须只返回一个字段。
--左边表达式使用operator对子查询结果的每一行进行一次计算和比较，其结果必须是布尔值。
--如果全部获得真值，ALL结果为"真"（包括子查询没有返回任何行的情况）。
--如果至少获得一个假值，则结果是"假"

--建表
DROP TABLE if exists test_expression_15_01 cascade;
DROP TABLE if exists test_expression_15_02 cascade;
CREATE TABLE test_expression_15_01
(
    c_id            INTEGER               NOT NULL,
    c_name            CHAR(16)              NOT NULL,
    c_class                VARCHAR(20)
);

CREATE TABLE test_expression_15_02
(
    c_gradeid            INTEGER               NOT NULL,
    c_id            INTEGER               ,
    c_grade         INTEGER,
    c_subject       varchar
);
insert into test_expression_15_01 values(101,'zhangsan1','101');
insert into test_expression_15_01 values(102,'zhangsan2','101');
insert into test_expression_15_01 values(103,'zhangsan3','101');
insert into test_expression_15_01 values(104,'zhangsan4','102');
insert into test_expression_15_01 values(105,'zhangsan5','102');
insert into test_expression_15_01 values(106,'zhangsan6','103');
insert into test_expression_15_02 values(1001,101,80,'语');
insert into test_expression_15_02 values(1002,102,90,'语');
insert into test_expression_15_02 values(1003,103,75,'语');
insert into test_expression_15_02 values(1004,104,58,'语');
insert into test_expression_15_02 values(1005,105,96,'语');
insert into test_expression_15_02 values(1006,106,68,'语');
insert into test_expression_15_02 values(1007,101,68,'数');
insert into test_expression_15_02 values(1008,102,85,'数');
insert into test_expression_15_02 values(1009,103,85,'数');
insert into test_expression_15_02 values(1010,104,54,'数');
insert into test_expression_15_02 values(1011,105,75,'数');
insert into test_expression_15_02 values(1012,106,45,'数');
insert into test_expression_15_02 values(1013,101,85,'英');
insert into test_expression_15_02 values(1014,102,54,'英');
insert into test_expression_15_02 values(1015,103,68,'英');
insert into test_expression_15_02 values(1016,104,86,'英');
insert into test_expression_15_02 values(1017,105,55,'英');
insert into test_expression_15_02 values(1018,106,97,'英');
insert into test_expression_15_02 values(1019,109,100,null);
insert into test_expression_15_02 values(1020,NULL,115,'英');

--子查询返回多个字段
SELECT c_name,c_class  FROM test_expression_15_01 WHERE c_id < all (SELECT c_grade,c_subject FROM test_expression_15_02 WHERE c_grade < 100);
SELECT c_name,c_class  FROM test_expression_15_01 WHERE c_id = all (SELECT c_grade,c_subject FROM test_expression_15_02 WHERE c_grade < 100);

--全真则为真
SELECT c_name,c_class  FROM test_expression_15_01 WHERE c_id <= all (SELECT c_id FROM test_expression_15_02 WHERE c_grade = 100);
SELECT c_name,c_class  FROM test_expression_15_01 WHERE c_id != all (SELECT c_id FROM test_expression_15_02 WHERE c_grade = 100);

--一假则为假
SELECT c_name,c_class  FROM test_expression_15_01 WHERE c_id > all (SELECT c_id FROM test_expression_15_02 WHERE c_grade < 200);
SELECT c_name,c_class  FROM test_expression_15_01 WHERE c_id >= all (SELECT c_id FROM test_expression_15_02 WHERE c_grade < 200);
SELECT c_name,c_class  FROM test_expression_15_01 WHERE c_id <> all (SELECT c_id FROM test_expression_15_02 WHERE c_grade < 200);

--无返回为假
SELECT c_name,c_class  FROM test_expression_15_01 WHERE c_id < all (SELECT c_id FROM test_expression_15_02 WHERE c_grade > 200);
SELECT c_name,c_class  FROM test_expression_15_01 WHERE c_id != all (SELECT c_id FROM test_expression_15_02 WHERE c_grade > 200);
SELECT c_name,c_class  FROM test_expression_15_01 WHERE c_id >= all (SELECT c_id FROM test_expression_15_02 WHERE c_grade > 200);

--环境清理
DROP TABLE if exists test_expression_15_01 cascade;
DROP TABLE if exists test_expression_15_02 cascade;