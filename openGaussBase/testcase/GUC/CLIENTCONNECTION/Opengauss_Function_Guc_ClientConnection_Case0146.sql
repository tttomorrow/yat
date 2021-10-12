-- @testpoint: 使用set方法设置参数extra_float_digits为无效值，合理报错
--查看默认值
show extra_float_digits;
--设置为浮点数，报错
set extra_float_digits to 5.56;
--设置为超范围值，报错
set extra_float_digits to -16;
set extra_float_digits to -4;
--设置为test，报错
set extra_float_digits to 'test';
--no need to clean