-- @testpoint: 创建带DEFERRABLE INITIALLY DEFERRED约束的表，插入重复值合理报错

DROP TABLE IF EXISTS tab_18;
CREATE TABLE IF not EXISTS tab_18
(id                      NUMBER(7)PRIMARY KEY DEFERRABLE INITIALLY DEFERRED,
name              VARCHAR2(20)
);

insert into tab_18 values(1,'小龙');
insert into tab_18 values(1,'小牛');
DROP TABLE IF EXISTS tab_18 CASCADE;

