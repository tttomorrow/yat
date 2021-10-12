-- @testpoint: opengauss比较操作符=，几何类型

-- 几何类型，比较的是面积、长度大小
SELECT box'(1,1),(2,3)' = box'(1,1),(2,2)';
SELECT box'(0,0),(3,3)' = box'(1,1),(4,4)';
SELECT circle'<(1,1),2>' = circle'<(1,1),3>';
SELECT circle'<(1,1),3>' = circle'<(2,2),3>';
SELECT lseg'(1,1),(2,5)' = lseg'(1,1),(2,3)';
SELECT lseg'(0,0),(2,3)' = lseg'(1,1),(2,3)';
SELECT path'(1,1),(2,2),(3,1),(2,0)' = path'(0,0),(1,1),(1,2),(0,1)';
SELECT path'(1,1),(4,4)' = path'(2,2),(5,4)';