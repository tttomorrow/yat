-- @testpoint: 函数substring_inner(string [from int] [for int])，截取子字符串，参数为无效值时，合理报错

--被截取文本为中文时
select substring_inner('你好中国', 2,3);
--被截取英文文本不带引号
select substring_inner(asdf, 1,3);
--第二个参数为非int类型时
select substring_inner('asdfg', a,3);

