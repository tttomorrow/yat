-- @testpoint: opengauss关键字read(非保留)，合理报错

drop table if exists test_035;
create table test_035(id int, name char(20));

--以隔离级别为READ COMMITTED，只读方式启动事务,insert语句报错
START TRANSACTION ISOLATION LEVEL READ COMMITTED READ ONLY;
SELECT * FROM test_035;
insert into test_035 values(1,'zhangsan');
SELECT * FROM test_035;
COMMIT;

--以隔离级别为READ COMMITTED，读/写方式启动事务    读写成功
START TRANSACTION ISOLATION LEVEL READ COMMITTED READ WRITE;
SELECT * FROM test_035;
insert into test_035 values(2,'lisi');
SELECT * FROM test_035;
COMMIT;

--开启一个事务，设置事务的隔离级别为READ COMMITTED，访问模式为READ ONLY,insert语句报错
START TRANSACTION;
SET LOCAL TRANSACTION ISOLATION LEVEL READ COMMITTED READ ONLY;
SELECT * FROM test_035;
insert into test_035 values(3,'wangwu');
COMMIT;

--开启一个事务，设置事务的隔离级别为READ COMMITTED，访问模式为READ WRITE  读写成功
START TRANSACTION;
SET LOCAL TRANSACTION ISOLATION LEVEL READ COMMITTED READ WRITE;
insert into test_035 values(3,'wangwu');
SELECT * FROM test_035;
COMMIT;

--清理环境
drop table test_035;