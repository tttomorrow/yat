-- @testpoint: set方法修改参数explain_dna_file为相对路径，合理报错
--查询默认
show explain_dna_file;
--设置，报错
SET explain_dna_file to 'test.csv';
--no need to clean