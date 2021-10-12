-- @testpoint: 函数substring_inner(string [from int] [for int])，截取子字符串，from int表示从第几个字符开始截取，for int表示截取几个字节

--参数是有效值
select substring_inner('adcde', 2,3);
select substring_inner('adcde123456', 6,3);
select substring_inner('adcde@23456', 6,3);
select substring_inner('adcde_23456', 6,3);
select substring_inner(12345, 2,3);
