-- @testpoint:创建表,部分用例合理报错
CREATE TABLE t_Opengauss_ANY_VALUE_Case0019_1(BT_COL1 INTEGER,BT_COL2 BLOB,BT_COL3 RAW,BT_COL4 BYTEA);
--插入数据
INSERT INTO t_Opengauss_ANY_VALUE_Case0019_1 VALUES(10,empty_blob(),HEXTORAW('DEADBEEF'),E'\\xDEADBEEF');
INSERT INTO t_Opengauss_ANY_VALUE_Case0019_1 VALUES(10,empty_blob(),HEXTORAW('DEADBEEF'),E'\\xDEADBEEF');
-- 查询
select any_value(BT_COL1333),any_value(BT_COL333) from t_Opengauss_ANY_VALUE_Case0019_1 group by BT_COL1,BT_COL2;
--清理环境
drop table t_Opengauss_ANY_VALUE_Case0019_1;
