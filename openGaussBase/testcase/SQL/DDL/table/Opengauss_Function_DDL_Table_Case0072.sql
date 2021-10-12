-- @testpoint: 创建表，并指定该表数据不写入预写日志

DROP TABLE IF EXISTS tab_18;

CREATE UNLOGGED TABLE tab_18
(id               NUMBER(7),
 name              VARCHAR2(20)
);
DROP TABLE IF EXISTS tab_18;
