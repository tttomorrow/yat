-- @testpoint: 插入数据，数据类型为时间间隔类型,违法唯一约束，合理报错
-- @modify at: 2020-11-16
--建表，指定一列是时间间隔型
DROP TABLE if exists PFA_dsitvl;
CREATE TABLE PFA_dsitvl(id int, dsval interval day(7) to second unique);
--插入数据
INSERT INTO PFA_dsitvl VALUES(1, '1231 12:3:4.1234');
--再次插入相同数据，合理报错
INSERT  INTO PFA_dsitvl VALUES(1, '1231 12:3:4.1234');
--插入成功
insert into PFA_dsitvl values(2,'P1231DT16H3.3333333S');
--合理报错
insert into PFA_dsitvl values(2,'P1231DT16H3.3333333S');
--插入数据，指定唯一约束列是null值，插入成功
INSERT INTO PFA_dsitvl VALUES(3, null);
INSERT INTO PFA_dsitvl VALUES(3, null);
INSERT INTO PFA_dsitvl VALUES(3, null);
--插入数据，指定唯一约束列是空字符串，插入成功
INSERT INTO PFA_dsitvl VALUES(3, '');
INSERT INTO PFA_dsitvl VALUES(3, '');
--删表
DROP TABLE if exists PFA_dsitvl cascade;


