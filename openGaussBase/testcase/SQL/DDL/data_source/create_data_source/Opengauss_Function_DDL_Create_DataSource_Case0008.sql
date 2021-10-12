-- @testpoint: 创建一个Data Source对象,含TYPE, VERSION, OPTIONS,不存在证书文件,合理报错
--$GAUSSHOME/bin目录下不存在datasource.key.cipher和datasource.key.rand文件，OPTIONS中出现password选项,合理报错
drop DATA SOURCE if exists ds_test8;
CREATE DATA SOURCE ds_test8 TYPE 'unknown' VERSION '11.2.3' OPTIONS (dsn 'openGauss', username 'dp', password 'Xiaxia@123', encoding '');


