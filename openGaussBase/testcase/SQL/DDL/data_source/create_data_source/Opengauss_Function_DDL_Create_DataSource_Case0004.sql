--  @testpoint:创建数据源对象，不含任何信息，名称超过63字节
--名称截取为63位
DROP DATA SOURCE if exists ds_test1qyytttgfvvbjnmkxjsojcdvdjfeijfeoijfoedwvjedivojdiokvjdte;
CREATE DATA SOURCE ds_test1qyytttgfvvbjnmkxjsojcdvdjfeijfeoijfoedwvjedivojdiokvjdte;
--查询创建的数据源对象信息(64位)
select srcname,srctype,srcversion,srcacl,srcoptions from PG_EXTENSION_DATA_SOURCE where srcname = 'ds_test1qyytttgfvvbjnmkxjsojcdvdjfeijfeoijfoedwvjedivojdiokvjdte';
--查询创建的数据源对象信息(63位)
select srcname,srctype,srcversion,srcacl,srcoptions from PG_EXTENSION_DATA_SOURCE where srcname = 'ds_test1qyytttgfvvbjnmkxjsojcdvdjfeijfeoijfoedwvjedivojdiokvjdt';
--删除创建的数据源对象
DROP DATA SOURCE ds_test1qyytttgfvvbjnmkxjsojcdvdjfeijfeoijfoedwvjedivojdiokvjdte;