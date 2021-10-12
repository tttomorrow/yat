--  @testpoint:opengauss关键字prepare(非保留)，创建一个预备语句，在EXECUTE语句中执行

--创建模式
DROP schema if exists tpcds;
CREATE schema tpcds;

CREATE TABLE tpcds.reason (
    CD_DEMO_SK          INTEGER          NOT NULL,
    CD_GENDER           character(16),
    CD_MARITAL_STATUS   character(100)
)
;
--插入数据
INSERT INTO tpcds.reason VALUES(51, 'AAAAAAAADDAAAAAA', 'reason 51');
select * from tpcds.reason;
--创建表reason_t1
CREATE TABLE tpcds.reason_t1 AS TABLE tpcds.reason;

--为一个INSERT语句创建预备语句
--表中插入语句
PREPARE insert_reason(integer,character(16),character(100)) AS INSERT INTO tpcds.reason_t1 VALUES($1,$2,$3);

--更新表数据
PREPARE update_reason AS  update  tpcds.reason_t1  set CD_DEMO_SK=CD_DEMO_SK*2;

--删除表数据
PREPARE delete_reason(integer) AS  delete from tpcds.reason_t1 where  CD_DEMO_SK=$1;  

--查询表数据
PREPARE select_reason_1(integer) AS  select * from tpcds.reason_t1 where  CD_DEMO_SK=$1;  

PREPARE select_reason_2(integer) AS  select * from tpcds.reason_t1 where  CD_DEMO_SK=$1 and cd_marital_status=$2;  

--执行预备语句
EXECUTE insert_reason(52, 'AAAAAAAADDAAAAAA', 'reason 52');
select * from  tpcds.reason_t1;
EXECUTE update_reason;
select * from  tpcds.reason_t1;
EXECUTE delete_reason(102);
select * from tpcds.reason_t1;
EXECUTE select_reason_1(1);
EXECUTE select_reason_1(104);
EXECUTE select_reason_2(104,'reason 52');

--删除表reason和reason_t1
DROP TABLE tpcds.reason;
DROP TABLE tpcds.reason_t1;
drop schema tpcds;



