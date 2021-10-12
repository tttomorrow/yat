-- @testpoint: alter system set方法设置参数xmlbinary值，合理报错
--查询默认
show xmlbinary;
--设置，报错
alter system set xmlbinary to hex;