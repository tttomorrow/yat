-- @testpoint: language赋USAGE权限查询USAGE权限返回为true
DROP USER IF EXISTS joe CASCADE;
CREATE USER joe PASSWORD 'Bigdata@123';
GRANT USAGE ON LANGUAGE sql TO joe;
select has_language_privilege ('joe', 'sql', 'USAGE');
DROP USER IF EXISTS joe CASCADE;