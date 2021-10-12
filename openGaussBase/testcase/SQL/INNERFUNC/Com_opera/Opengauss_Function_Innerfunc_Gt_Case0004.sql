-- @testpoint: opengauss比较操作符>=，二进制类型

-- 二进制类型,比较的是数值大小
SELECT 'ABCDEF'::RAW >= 'ABCDEE'::RAW;
SELECT 'abcdef'::RAW >= 'ABCDEF'::RAW;
