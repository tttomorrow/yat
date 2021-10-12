-- @testpoint: opengauss比较操作符=，位串类型

-- 位串类型,长度不一致时取短串的长度对长串进行左边的截取，然后再进行二进制的比较
SELECT B'00000' = B'00001';
SELECT B'00001' = B'001';
SELECT B'11111' = B'01111';
SELECT B'00000'::bit varying = B'00001'::bit varying;
SELECT B'00001'::bit varying = B'001'::bit;
SELECT B'11111'::bit= B'01111'::bit varying;
