-- @testpoint: fetch抓取最后一行数据

drop TABLE if EXISTS test_2;
CREATE TABLE test_2(ID INT,NAME CHAR(20));
INSERT INTO test_2 VALUES(1,'Lily'),(2,'Tom'),(3,'Maria');
START TRANSACTION;
CURSOR cursor1 FOR SELECT * FROM test_2 ORDER by name;
FETCH  LAST from CURSOR1;
CLOSE cursor1;
end;
drop TABLE test_2;