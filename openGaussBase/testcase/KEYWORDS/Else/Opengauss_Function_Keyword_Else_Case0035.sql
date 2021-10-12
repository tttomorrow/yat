-- @testpoint: else用于条件表达式中
--case when之后的条件都为真,返回结果是then之后的值
drop table if exists case_when_t1;
CREATE TABLE case_when_t1(CW_COL1 INT);
INSERT INTO case_when_t1 VALUES (1), (2), (3);
SELECT * FROM case_when_t1;
SELECT CW_COL1, CASE WHEN CW_COL1=1 THEN 'one' WHEN CW_COL1=2 THEN 'two' ELSE 'other' END FROM case_when_t1 ORDER BY 1;
drop table case_when_t1;
--case when之后的条件第一个为假，返回else后的值other
drop table if exists case_when_t1;
CREATE TABLE case_when_t1(CW_COL1 INT);
INSERT INTO case_when_t1 VALUES (1), (2), (3);
SELECT * FROM case_when_t1;
SELECT CW_COL1, CASE WHEN CW_COL1=4 THEN 'four' WHEN CW_COL1=2 THEN 'two' ELSE 'other' END FROM case_when_t1 ORDER BY 1;
drop table case_when_t1;
--case when之后的条件都为假,返回else后的值other
drop table if exists case_when_t1;
CREATE TABLE case_when_t1(CW_COL1 INT);
INSERT INTO case_when_t1 VALUES (1), (2), (3);
SELECT * FROM case_when_t1;
SELECT CW_COL1, CASE WHEN CW_COL1=5 THEN 'five' WHEN CW_COL1=4 THEN 'two' ELSE 'other' END FROM case_when_t1 ORDER BY 1;
drop table if exists case_when_t1;