--  @testpoint: 创建一个同义词对象，验证大小写。
--同义词是数据库对象的别名，用于记录与其他数据库对象名间的映射关系，用户可以使用同义词访问关联的数据库对象。
CREATE OR REPLACE SYNONYM vi for view_3;
CREATE OR REPLACE SYNONYM AD FOR VIEW_3;
CREATE OR REPLACE SYNONYM ad FOR FALSE_3;
CREATE OR REPLACE SYNONYM AD FOR view_3;
CREATE OR REPLACE SYNONYM ad FOR false_3;
select * from ad;
select * from AD;
select synobjname from pg_synonym where synname in ('ad');
select synobjname from pg_synonym where synname in ('AD');