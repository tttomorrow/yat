-- @testpoint: 使用alter system set方法设置参数extra_float_digits，合理报错
--查看默认值
show extra_float_digits;
--设置，报错
alter system set extra_float_digits to 3;
alter system set extra_float_digits to -15;
--no need to clean