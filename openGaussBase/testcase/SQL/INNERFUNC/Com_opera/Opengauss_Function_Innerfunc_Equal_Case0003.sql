-- @testpoint: opengauss比较操作符=，布尔类型

-- 布尔类型,真大于假
SELECT 'y'::BOOLEAN = 't'::BOOLEAN;
SELECT 'f'::BOOLEAN = 'n'::BOOLEAN;
SELECT 'n'::BOOLEAN = 'f'::BOOLEAN;
SELECT 'yes'::BOOLEAN = 'no'::BOOLEAN;
SELECT 'yes'::BOOLEAN = 'y'::BOOLEAN;
SELECT 'yes'::BOOLEAN = 'TRUE'::BOOLEAN;
SELECT '0'::BOOLEAN = 'false'::BOOLEAN;