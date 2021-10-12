-- @testpoint: md5函数入参给二进制类型blog,合理报错
SELECT md5(empty_blob());