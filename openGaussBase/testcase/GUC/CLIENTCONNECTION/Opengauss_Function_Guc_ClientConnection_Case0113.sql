-- @testpoint: alter system set方法设置参数xmloption值，合理报错
--查询默认
show xmloption;
--设置，报错
alter system set xmloption to document;