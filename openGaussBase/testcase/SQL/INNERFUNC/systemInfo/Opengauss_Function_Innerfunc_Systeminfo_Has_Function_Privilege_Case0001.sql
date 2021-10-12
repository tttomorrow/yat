-- @testpoint: 给表的某一列赋予权限查询任一列是否有该权限
DROP USER IF EXISTS joe CASCADE;
CREATE USER joe PASSWORD 'Bigdata@123';

select has_function_privilege('joe', 'age(timestamp, timestamp)','EXECUTE');
DROP USER IF EXISTS joe CASCADE;