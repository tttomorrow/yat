-- @testpoint: opengauss比较操作符<=，字符类型
-- 字符类型,比较的是ascii码值，长度相同，挨个比较ascii码值，长度不同以短的长度去比较，如果截取的和短的一样则长串大
select 'abc'::char(5) <= 'stude'::char(5);
select 'student'::char(5) <= 'stu'::char(5);
select 'student'::char(5) <= 'student'::nchar(5);
select 'student'::char(5) <= 'stu'::CHARACTER(5);
select 'student'::VARCHAR(5) <= 'student'::VARCHAR(5);
select 'students'::CHARACTER VARYING(5) <= 'student'::CHARACTER VARYING(5);
select 'students'::VARCHAR2(5) <= 'student'::VARCHAR2(5);
select 'students'::text <= 'student'::text;