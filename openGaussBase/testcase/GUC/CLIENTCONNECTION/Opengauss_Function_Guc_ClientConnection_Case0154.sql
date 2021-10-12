-- @testpoint: set方法设置lc_monetary为无效值，合理报错
--查看默认值
show lc_monetary;
--设置无效值，报错
set lc_monetary to 'test';
set lc_monetary to '1234';
set lc_monetary to 'en_US$#';
--no need to clean