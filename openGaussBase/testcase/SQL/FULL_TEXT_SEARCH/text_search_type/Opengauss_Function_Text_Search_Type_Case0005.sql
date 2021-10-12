--  @testpoint:建表指定数据类型是tsvector和tsquery类型
DROP TABLE if EXISTS test_1;
CREATE TABLE test_1(name tsvector,comm tsquery );
--插入成功，原样输出
INSERT into test_1 values('Fat a cat','fat & cats');
INSERT INTO test_1 VALUES('fat:2A','cat | dog & !cats');
--插入不合理的值，报错
INSERT INTO test_1 VALUES('tomatoes wow','cat and dog');
SELECT * from test_1;
DROP TABLE test_1;