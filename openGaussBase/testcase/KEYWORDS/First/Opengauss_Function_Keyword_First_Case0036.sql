-- @testpoint: first用于抓取游标中的第一行数据

drop TABLE if EXISTS test_1;
CREATE TABLE test_1(ID INT,NAME CHAR(20));
INSERT INTO test_1 VALUES(1,'Lily'),(2,'Tom'),(3,'Maria');
START TRANSACTION;
CURSOR cursor1 FOR SELECT * FROM test_1 ORDER by name;
FETCH FIRST from CURSOR1;
CLOSE cursor1;
end;
drop TABLE test_1;