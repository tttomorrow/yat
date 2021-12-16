-- @testpoint: opengauss比较操作符=，二进制类型

-- 二进制类型,比较的是数值大小
SELECT '101010101010'::blob = '101010101009'::blob;
SELECT '101010101010'::blob = '101010101010'::blob;
SELECT 'ABCDEF'::RAW = 'ABCDEE'::RAW;
SELECT 'abcdef'::RAW = 'ABCDEF'::RAW;
