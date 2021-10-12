--创建枚举类型,标签名不超过64位
drop type if exists bugstatus;
CREATE TYPE bugstatus AS ENUM ('create', 'modify', 'closed');
--标签名等于64位
drop type if exists bugstatus1 cascade;
CREATE TYPE bugstatus1 AS ENUM ('createcshksjdbnskjcbnskjcbnsjcbncbsxkcbscbKHWEIDHBIWFHBSBCISAZDQ');
--标签名大于64位，合理报错，报错又提示标签名必须在1-63字节
drop type if exists bugstatus1 cascade;
CREATE TYPE bugstatus1 AS ENUM ('createcshksjdbnskjcbnskjcbnsjcbncbsxkcbscbKHWEIDHBIWFHBSBCISAZDQF');
--建表，指定其中一列是枚举类型
CREATE TABLE t1_test(a int, b bugstatus1);
--插入数据，插入64位的标签，报错
INSERT INTO t1_test values(1,'createcshksjdbnskjcbnskjcbnsjcbncbsxkcbscbKHWEIDHBIWFHBSBCISAZDQ');
--插入数据，插入63位的标签，成功
INSERT INTO t1_test values(1,'createcshksjdbnskjcbnskjcbnsjcbncbsxkcbscbKHWEIDHBIWFHBSBCISAZD');
select * from t1_test;

--删除类型
drop type if exists bugstatus;