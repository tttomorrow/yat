-- @testpoint: language赋所有权限USAGE返回为true
DROP USER IF EXISTS joe CASCADE;
CREATE USER joe PASSWORD 'Bigdata@123';
GRANT ALL PRIVILEGES ON LANGUAGE sql TO joe;
select has_language_privilege ('joe', 'sql', 'USAGE');
DROP USER IF EXISTS joe CASCADE;