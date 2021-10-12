-- @testpoint: 在事务中创建修改删除数据库失败,合理报错

START TRANSACTION;
create database test_db;
end;
create database test_db;
START TRANSACTION;
ALTER DATABASE test_db with CONNECTION LIMIT 2;
end;
START TRANSACTION;
drop database test_db;
end;

--tearDown
drop database if exists test_db;