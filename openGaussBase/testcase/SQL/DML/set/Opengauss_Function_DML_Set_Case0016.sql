--  @testpoint：依次设置时区为local、default，timezone参数值不变
--设置时区为local
set session time zone local;
show time zone;
--设置时区为default
set  time zone default;
show time zone;

--设置时区为local,default，合理报错
 set time zone local,default;

 --设置时区是defaults，合理报错
 set time zone defaults;