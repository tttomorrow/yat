-- @testpoint: language不赋权限查询USAGE权限返回为true（本身带有sql语言权限）
DROP USER IF EXISTS joe CASCADE;
CREATE USER joe PASSWORD 'Bigdata@123';
select has_language_privilege ('joe', 'sql', 'USAGE');
DROP USER IF EXISTS joe CASCADE;