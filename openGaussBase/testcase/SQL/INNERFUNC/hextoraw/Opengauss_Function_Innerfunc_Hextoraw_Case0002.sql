-- @testpoint: hextoraw函数测试，参数为无效值，合理报错
--将一个十六进制构成的字符串转换为二进制
--报错
select hextoraw();
select hextoraw(-1);
--函数使用成功
select hextoraw(0);
select hextoraw(2);
select hextoraw('');