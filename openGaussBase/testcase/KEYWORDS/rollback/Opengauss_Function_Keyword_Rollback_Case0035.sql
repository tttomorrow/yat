--  @testpoint:opengauss关键字rollback(非保留)，回滚当前事务并取消当前事务中的所有更新
--创建表
drop table if exists test_035;
create table test_035(id int, name char(20));

--开启事务并回滚
START TRANSACTION ;
SELECT * FROM test_035;
insert into test_035 values(2,'lisi');
SELECT * FROM test_035;

--回滚
ROLLBACK;

--查看表数据
SELECT * FROM test_035;

--开启事务并提交
START TRANSACTION ;
SELECT * FROM test_035;
insert into test_035 values(2,'lisi');
SELECT * FROM test_035;
COMMIT;

--清理环境
drop table test_035;
