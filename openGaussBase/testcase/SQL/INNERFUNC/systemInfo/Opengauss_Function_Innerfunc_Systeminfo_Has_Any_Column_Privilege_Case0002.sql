-- @testpoint: 给表的任意一列都没有赋予某权限查询表内是否有该权限
DROP USER IF EXISTS joe CASCADE;
CREATE USER joe PASSWORD 'Bigdata@123';
DROP table IF EXISTS table_test001;
create table table_test001(c int,d int); 
GRANT select (c),update (d) ON table_test001 TO joe;
SELECT has_any_column_privilege('joe', 'table_test001','INSERT');
DROP USER IF EXISTS joe CASCADE;
DROP table IF EXISTS table_test001;