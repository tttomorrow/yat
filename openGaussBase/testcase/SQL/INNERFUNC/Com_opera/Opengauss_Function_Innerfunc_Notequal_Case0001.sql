-- @testpoint: opengauss比较操作符<>,字符类型
-- 字符类型,比较的是ascii码值
select 'abc'::char(5) <> 'abc'::char(5);
select 'student'::char(5) <> 'stu'::char(5);
select 'student'::char(5) <> 'student'::nchar(5);
select 'student'::char(5) <> 'student'::VARCHAR(5);
select 'students'::CHARACTER VARYING(5) <> 'student'::VARCHAR2(5);
select 'students'::VARCHAR2(5) <> 'student'::VARCHAR2(5);
select text'students' <> clob'students';