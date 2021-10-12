-- @testpoint: 转换字符为二进制再转换为文本数据，参数不添加引号，合理报错
SELECT encode(test,'base64');
SELECT encode(11010011, 'base64');
