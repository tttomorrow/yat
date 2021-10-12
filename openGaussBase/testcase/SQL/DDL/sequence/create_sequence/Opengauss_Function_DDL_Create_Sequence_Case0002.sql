--  @testpoint:序列名与同一模式下的对象名相同，合理报错
--testpoint1:建表
drop table if exists test_t1;
create table test_t1(id int);
--创建序列，序列名与同一模式下的表名相同，合理报错
CREATE SEQUENCE test_t1;
--删表
drop table test_t1;
--testpoint2:序列名相同，合理报错
drop SEQUENCE if exists test_t2;
CREATE SEQUENCE test_t2;
--再次创建同名序列
CREATE SEQUENCE test_t2;
--删除序列
drop SEQUENCE test_t2;
--testpoint3:序列名与视图名相同，合理报错
CREATE VIEW test_myView AS
    SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
--创建序列
CREATE SEQUENCE test_myView;
--删除序列
drop view test_myView;
--testpoint4:序列名与索引名相同，合理报错
--建表
drop table if exists ship_mode_t1;
CREATE TABLE ship_mode_t1
(
    SM_SHIP_MODE_SK           INTEGER               NOT NULL,
    SM_SHIP_MODE_ID           CHAR(16)              NOT NULL,
    SM_TYPE                   CHAR(30)                      ,
    SM_CODE                   CHAR(10)                      ,
    SM_CARRIER                CHAR(20)                      ,
    SM_CONTRACT               CHAR(20)
) ;
--在表ship_mode_t1上的SM_SHIP_MODE_SK字段上创建唯一索引
CREATE UNIQUE INDEX ds_ship_mode_t1_index1 ON ship_mode_t1(SM_SHIP_MODE_SK);
--创建于索引名同名的序列
CREATE SEQUENCE ds_ship_mode_t1_index1;
--删除表
drop table ship_mode_t1;
--testpoint5:序列名与用户名相同
--创建用户
drop user if exists test_user1;
create user test_user1 password 'Xiaxia@123';
--创建同名序列，创建成功
drop SEQUENCE if exists test_user1;
create SEQUENCE test_user1;
--查询序列信息
select sequence_name from test_user1 where sequence_name = 'test_user1';
--删除用户
drop user test_user1;
--删除序列
drop SEQUENCE test_user1;