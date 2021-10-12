-- @testpoint: opengauss比较操作符!=,几何类型
-- 几何类型，比较的是面积大小
SELECT circle'<(1,1),2>' != circle'<(1,1),3>';
SELECT circle'<(1,1),3>' != circle'<(2,2),3>';
SELECT lseg'(1,1),(2,5)' != lseg'(1,1),(2,3)';
SELECT lseg'(0,0),(2,3)' != lseg'(1,1),(2,3)';
select point(1,2) != point(3,2) as result;